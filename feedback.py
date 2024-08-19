from textblob import TextBlob
import matplotlib.pyplot as plt

def analyze_sentiment(text):
    """Analyzes the sentiment of the given text and returns the polarity."""
    blob = TextBlob(text)
    return blob.sentiment.polarity

def main():
    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
    count = int(input("How many texts would you like to analyze? "))

    for i in range(count):
        user_input = input(f"Enter text {i+1}: ")
        polarity = analyze_sentiment(user_input)
        if polarity > 0:
            sentiments['positive'] += 1
            print("Result: Positive")
        elif polarity < 0:
            sentiments['negative'] += 1
            print("Result: Negative")
        else:
            sentiments['neutral'] += 1
            print("Result: Neutral")

    # Visualization
    labels = sentiments.keys()
    sizes = [sentiments[label] for label in labels]
    colors = ['green', 'red', 'gray']  # Colors for positive, negative, neutral
    explode = (0.1, 0.1, 0.1)  # "explode" the slices

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Sentiment Analysis Results')
    plt.show()

if __name__ == "__main__":
    main()

