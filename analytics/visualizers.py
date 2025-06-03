import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot
import pandas as pd
from django.template.loader import render_to_string


class ChartGenerator:
    """Create beautiful, interactive charts! 🎨"""

    def create_rating_distribution_chart(self, rating_data):
        """Create a bar chart for rating distribution"""
        ratings = list(range(1, 6))
        counts = [rating_data.get(str(i), 0) for i in ratings]

        fig = go.Figure(data=[
            go.Bar(
                x=ratings,
                y=counts,
                marker_color=['#ff4444', '#ff8800', '#ffbb00', '#88bb00', '#44bb00'],
                text=counts,
                textposition='auto',
            )
        ])

        fig.update_layout(
            title='Rating Distribution',
            xaxis_title='Rating (1-5)',
            yaxis_title='Number of Responses',
            template='plotly_white'
        )

        return plot(fig, output_type='div', include_plotlyjs=False)

    def create_professor_comparison_chart(self, comparison_data):
        """Create comparison chart for multiple professors"""
        df = pd.DataFrame(comparison_data)

        fig = px.scatter(
            df,
            x='total_responses',
            y='average_rating',
            size='total_responses',
            color='sentiment',
            hover_name='professor_name',
            title='Professor Performance Comparison',
            color_continuous_scale='RdYlGn'
        )

        fig.update_layout(template='plotly_white')
        return plot(fig, output_type='div', include_plotlyjs=False)

    def create_department_trend_chart(self, department_data):
        """Create trend chart for department performance over time"""
        df = pd.DataFrame(department_data)

        fig = px.line(
            df,
            x='date',
            y='average_rating',
            title='Department Performance Trend',
            markers=True
        )

        fig.update_layout(template='plotly_white')
        return plot(fig, output_type='div', include_plotlyjs=False)

    def create_sentiment_gauge(self, sentiment_score):
        """Create a gauge chart for sentiment"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=sentiment_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Sentiment Score"},
            gauge={
                'axis': {'range': [-1, 1]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [-1, -0.5], 'color': "lightgray"},
                    {'range': [-0.5, 0.5], 'color': "gray"},
                    {'range': [0.5, 1], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 0.9
                }
            }
        ))

        return plot(fig, output_type='div', include_plotlyjs=False)


class WordCloudGenerator:
    """Generate word clouds from text feedback"""

    def generate_wordcloud(self, keywords, weights=None):
        """Generate word cloud from keywords"""
        # Implementation for word cloud generation
        # You'll use the wordcloud library here
        pass