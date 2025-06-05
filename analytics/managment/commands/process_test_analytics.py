from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from collections import Counter
from textblob import TextBlob
from analytics.models import TempProfessor, TempSurveyResponse, ProfessorAnalytics, DepartmentAnalytics
from django.db.models import Avg, Count


class Command(BaseCommand):
    help = 'Process test analytics data'

    def handle(self, *args, **options):
        self.stdout.write("🧠 Processing analytics like a GENIUS!")

        # Process analytics for each day in the last 30 days
        for day_offset in range(30):
            current_date = timezone.now().date() - timedelta(days=day_offset)
            self.process_day_analytics(current_date)

        self.stdout.write("✨ Analytics processing complete!")
        self.stdout.write("🎯 Check your Django admin or create views to see the results!")

    def process_day_analytics(self, date):
        """Process analytics for a specific date"""
        professors = TempProfessor.objects.all()

        for professor in professors:
            # Get responses for this professor on this date
            responses = TempSurveyResponse.objects.filter(
                professor_id=professor.id,
                created_at__date=date
            )

            if not responses.exists():
                continue

            # Calculate basic stats
            total_responses = responses.count()
            avg_rating = responses.aggregate(avg=Avg('rating'))['avg']

            # Rating distribution
            rating_dist = {}
            for i in range(1, 6):
                rating_dist[str(i)] = responses.filter(rating=i).count()

            # Text analysis
            text_responses = responses.filter(
                text_feedback__isnull=False
            ).exclude(text_feedback='').values_list('text_feedback', flat=True)

            sentiment_score = self.analyze_sentiment(text_responses)
            keywords = self.extract_keywords(text_responses)

            # Save professor analytics
            ProfessorAnalytics.objects.update_or_create(
                professor_id=professor.id,
                date=date,
                defaults={
                    'professor_name': professor.name,
                    'total_responses': total_responses,
                    'average_rating': round(avg_rating, 2),
                    'rating_distribution': rating_dist,
                    'sentiment_score': round(sentiment_score, 3),
                    'common_keywords': keywords[:10]
                }
            )

        # Process department analytics
        departments = TempProfessor.objects.values_list('department', flat=True).distinct()

        for department in departments:
            dept_professors = TempProfessor.objects.filter(department=department)
            dept_responses = TempSurveyResponse.objects.filter(
                professor_id__in=dept_professors.values_list('id', flat=True),
                created_at__date=date
            )

            if not dept_responses.exists():
                continue

            total_responses = dept_responses.count()
            avg_rating = dept_responses.aggregate(avg=Avg('rating'))['avg']

            # Top and bottom performers
            prof_ratings = []
            for prof in dept_professors:
                prof_responses = dept_responses.filter(professor_id=prof.id)
                if prof_responses.exists():
                    prof_avg = prof_responses.aggregate(avg=Avg('rating'))['avg']
                    prof_ratings.append({
                        'id': prof.id,
                        'name': prof.name,
                        'rating': round(prof_avg, 2)
                    })

            prof_ratings.sort(key=lambda x: x['rating'], reverse=True)
            top_profs = prof_ratings[:3]
            bottom_profs = prof_ratings[-3:]

            DepartmentAnalytics.objects.update_or_create(
                department=department,
                date=date,
                defaults={
                    'total_responses': total_responses,
                    'average_rating': round(avg_rating, 2),
                    'top_professors': top_profs,
                    'bottom_professors': bottom_profs
                }
            )

    def analyze_sentiment(self, text_list):
        """Analyze sentiment of text feedback"""
        if not text_list:
            return 0.0

        sentiments = []
        for text in text_list:
            if text:
                try:
                    blob = TextBlob(text)
                    sentiments.append(blob.sentiment.polarity)
                except:
                    continue

        return sum(sentiments) / len(sentiments) if sentiments else 0.0

    def extract_keywords(self, text_list):
        """Extract common keywords from feedback"""
        if not text_list:
            return []

        # Simple keyword extraction
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is',
                      'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                      'could', 'should', 'may', 'might', 'can', 'cannot', 'very', 'too', 'so', 'just', 'now', 'than',
                      'only', 'even', 'also', 'back', 'after', 'use', 'her', 'our', 'out', 'day', 'get', 'has', 'him',
                      'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let',
                      'put', 'say', 'she', 'too', 'use'}

        all_words = []
        for text in text_list:
            if text:
                words = [word.lower().strip('.,!?";') for word in text.split()
                         if len(word) > 3 and word.lower() not in stop_words and word.isalpha()]
                all_words.extend(words)

        counter = Counter(all_words)
        return [word for word, count in counter.most_common(15)]

