import pandas as pd
file_path = 'heart.csv'
heart_data = pd.read_csv(file_path)
print(heart_data.head())
print(heart_data.describe())
print(heart_data.info())
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# Encode categorical features
categorical_features = heart_data.select_dtypes(include=['object']).columns
encoders = {feature: LabelEncoder() for feature in categorical_features}
for feature in categorical_features:
    heart_data[feature] = encoders[feature].fit_transform(heart_data[feature])

# Normalize numerical features, excluding the target variable 'HeartDisease'
numerical_features = heart_data.select_dtypes(include=['float64', 'int64']).columns
numerical_features = numerical_features.drop('HeartDisease')
standard_scaler = StandardScaler()
heart_data[numerical_features] = standard_scaler.fit_transform(heart_data[numerical_features])

# Split the data into training and testing sets
X_features = heart_data.drop(columns=['HeartDisease'])
y_target = heart_data['HeartDisease']
X_train_set, X_test_set, y_train_set, y_test_set = train_test_split(X_features, y_target, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

classifier_models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier()
}
# Train and evaluate models
evaluation_results = {}
for classifier_name, classifier in classifier_models.items():
    print(f"Training {classifier_name}...")
    classifier.fit(X_train_set, y_train_set)
    y_predicted = classifier.predict(X_test_set)
    model_accuracy = accuracy_score(y_test_set, y_predicted)
    model_report = classification_report(y_test_set, y_predicted, output_dict=True)
    model_confusion_matrix = confusion_matrix(y_test_set, y_predicted)

    evaluation_results[classifier_name] = {
        "accuracy": model_accuracy,
        "classification_report": model_report,
        "confusion_matrix": model_confusion_matrix
    }
for classifier_name, results in evaluation_results.items():
    confusion_matrix = results["confusion_matrix"]
    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Predicted Negative', 'Predicted Positive'],
                yticklabels=['Actual Negative', 'Actual Positive'])
    plt.title(f'Confusion Matrix - {classifier_name}')
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.show()
    from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 8))

# Plot ROC curve for Logistic Regression
classifier_name = "Logistic Regression"
results = evaluation_results[classifier_name]
y_test = y_test_set
y_pred_proba = classifier_models[classifier_name].predict_proba(X_test_set)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'{classifier_name} (AUC = {roc_auc:.2f})')

# Plot ROC curve for Random Forest
classifier_name = "Random Forest"
results = evaluation_results[classifier_name]
y_test = y_test_set
y_pred_proba = classifier_models[classifier_name].predict_proba(X_test_set)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'{classifier_name} (AUC = {roc_auc:.2f})')

# Plot random guessing line
plt.plot([0, 1], [0, 1], linestyle='--', color='grey', label='Random Guessing')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()
# Display results for Logistic Regression
classifier_name = "Logistic Regression"
result = evaluation_results[classifier_name]
print(f"Model: {classifier_name}")
print(f"Accuracy: {result['accuracy']:.2f}")
print("\nConfusion Matrix:")
print(result['confusion_matrix'])
print("\n")

# Display results for Random Forest
classifier_name = "Random Forest"
result = evaluation_results[classifier_name]
print(f"Model: {classifier_name}")
print(f"Accuracy: {result['accuracy']:.2f}")
print("\nConfusion Matrix:")
print(result['confusion_matrix'])
# Save the best model (based on accuracy)
top_model_name = max(evaluation_results, key=lambda name: evaluation_results[name]['accuracy'])
top_model = classifier_models[top_model_name]
print(f"Best Model: {top_model_name} with Accuracy: {evaluation_results[top_model_name]['accuracy']}")

with open('best_heart_disease_model.pkl', 'wb') as f:
    pickle.dump(top_model, f)