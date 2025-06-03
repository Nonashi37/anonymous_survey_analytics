import pandas as pd
from django.db.models import Avg, Count, Q
from textblob import TextBlob
from collections import Counter
from surveys.models import SurveyResponse, Professor, Course
from .models import ProfessorAnalytics, DepartmentAnalytics, DailyAnalytics


class SurveyAnalyzer:
    """The brain of your analytics system! 🧠"""

    def __init__(self, date=None):
        self.date = date or timezone.now().date()

    def analyze_professor(self, professor_id):
        """Analyze individual professor performance"""
        responses = SurveyResponse.objects.filter(
            survey__professor_id=professor_id,
            created_at__date=self.date
        )

        if not responses.exists():
            return None

        # Basic stats
        total_responses = responses.count()
        avg_rating = responses.aggregate(Avg('rating'))['rating__avg']

        # Rating distribution
        rating_dist = {}
        for i in range(1, 6):
            rating_dist[i] = responses.filter(rating=i).count()

        # Sentiment analysis of text feedback
        text_responses = responses.filter(
            text_feedback__isnull=False
        ).values_list('text_feedback', flat=True)

        sentiment_score = self._analyze_sentiment(text_responses)
        keywords = self._extract_keywords(text_responses)

        # Save to database
        analytics, created = ProfessorAnalytics.objects.update_or_create(
            professor_id=professor_id,
            date=self.date,
            defaults={
                'total_responses': total_responses,
                'average_rating': avg_rating,
                'rating_distribution': rating_dist,
                'sentiment_score': sentiment_score,
                'common_keywords': keywords[:10]  # Top 10 keywords
            }
        )

        return analytics

    def analyze_department(self, department):
        """Analyze department performance"""
        professors = Professor.objects.filter(department=department)
        responses = SurveyResponse.objects.filter(
            survey__professor__in=professors,
            created_at__date=self.date
        )

        total_responses = responses.count()
        avg_rating = responses.aggregate(Avg('rating'))['rating__avg'] or 0

        # Top and bottom performers
        prof_ratings = []
        for prof in professors:
            prof_responses = responses.filter(survey__professor=prof)
            if prof_responses.exists():
                prof_avg = prof_responses.aggregate(Avg('rating'))['rating__avg']
                prof_ratings.append({'id': prof.id, 'name': prof.name, 'rating': prof_avg})

        prof_ratings.sort(key=lambda x: x['rating'], reverse=True)
        top_profs = prof_ratings[:5]
        bottom_profs = prof_ratings[-5:]

        analytics, created = DepartmentAnalytics.objects.update_or_create(
            department=department,
            date=self.date,
            defaults={
                'total_responses': total_responses,
                'average_rating': avg_rating,
                'top_professors': top_profs,
                'bottom_professors': bottom_profs
            }
        )

        return analytics

    def _analyze_sentiment(self, text_list):
        """Analyze sentiment of text feedback"""
        if not text_list:
            return 0.0

        sentiments = []
        for text in text_list:
            if text:
                blob = TextBlob(text)
                sentiments.append(blob.sentiment.polarity)

        return sum(sentiments) / len(sentiments) if sentiments else 0.0

    def _extract_keywords(self, text_list):
        """Extract common keywords from feedback"""
        if not text_list:
            return []

        all_words = []
        for text in text_list:
            if text:
                # Simple keyword extraction (you can make this more sophisticated)
                words = [word.lower() for word in text.split()
                         if len(word) > 3 and word.isalpha()]
                all_words.extend(words)

        counter = Counter(all_words)
        return [word for word, count in counter.most_common(20)]


class ComparativeAnalyzer:
    """Compare different entities - professors, departments, time periods"""

    def compare_professors(self, professor_ids, start_date, end_date):
        """Compare multiple professors over time period"""
        comparison_data = []

        for prof_id in professor_ids:
            analytics = ProfessorAnalytics.objects.filter(
                professor_id=prof_id,
                date__range=[start_date, end_date]
            )

            if analytics.exists():
                avg_rating = analytics.aggregate(Avg('average_rating'))['average_rating__avg']
                total_responses = sum(a.total_responses for a in analytics)

                comparison_data.append({
                    'professor_id': prof_id,
                    'professor_name': Professor.objects.get(id=prof_id).name,
                    'average_rating': round(avg_rating, 2),
                    'total_responses': total_responses,
                    'sentiment': analytics.aggregate(Avg('sentiment_score'))['sentiment_score__avg']
                })

        return comparison_data