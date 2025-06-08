from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Vectorizar texto
vectorizer = TfidfVectorizer(
    token_pattern=r"(?u)\b\w\w+\b",
    max_features=5000
)
X = vectorizer.fit_transform(df['payload'])
y = df['label']

# Entrenar modelo
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=30,
    random_state=42
)
model.fit(X_train, y_train)