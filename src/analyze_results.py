import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, preds)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Legit','Phishing'], yticklabels=['Legit','Phishing'])
plt.xlabel('Predicted'); plt.ylabel('Actual')
plt.savefig('results/confusion_matrix.png')
importances = best_model.feature_importances_
for name, score in sorted(zip(X.columns, importances), key=lambda x: -x[1]):
    print(name, round(score, 3))