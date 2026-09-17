# my_Repo
small capstone project
Interpretation 1:
This chart clearly illustrates a significant disparity in survival rates. Women, especially those in 1st and 2nd class, had a much higher chance of survival than men across all classes. This suggests that the "women and children first" policy was likely implemented, with social status (pclass) also playing a crucial role.
Interpretation 2:
Children (0-12 years) generally show a higher survival rate compared to teenagers and adults. This further supports the "women and children first" directive during the evacuation. The survival rate then tends to decrease for adults and seniors, indicating age was also a factor in rescue priority.
Interpretation 3:
Passengers who embarked from Cherbourg ('C') had a noticeably higher survival rate compared to those from Southampton ('S') and Queenstown ('Q'). This could be indirectly linked to passenger class distribution at each port, as Cherbourg passengers might have had a higher proportion of first-class passengers. This again highlights the importance of social status in survival.
Interpretation 4:
This violin plot clearly shows that passengers who paid higher fares, predominantly those in 1st class, had a much higher likelihood of survival. Within each passenger class, survivors generally paid higher fares than non-survivors. This reinforces the argument that economic status, often correlated with ticket fare and passenger class, was a major determinant of who survived the disaster.

	   Model     Accuracy	Precision (0)	Recall (0)	F1-Score (0)	Precision (1)	Recall (1)	F1-Score (1)	AUC 								
Logistic Regression	0.814607	0.823529	0.890909	0.855895	0.796610	0.691176	0.740157	0.859893
Decision Tree	0.747191	0.751938	0.881818	0.811715	0.734694	0.529412	0.615385	0.825869
Random Forest	0.797753	0.813559	0.872727	0.842105	0.766667	0.676471	0.718750	0.816979
Logistic Regression (Balanced)	0.792135	0.834862	0.827273	0.831050	0.724638	0.735294	0.729927	0.861631
Logistic Regression (SMOTE)	0.797753	0.836364	0.836364	0.836364	0.735294	0.735294	0.735294	0.866310

Classifier Recommendation
Based on the detailed evaluation, I would recommend deploying the Logistic Regression (SMOTE) model. While all models performed reasonably well, Logistic Regression (SMOTE) achieved the highest F1-Score for the 'survived' class (0.74) and the highest AUC (0.87), indicating a superior balance between precision and recall for the minority class and overall better discriminative power. This improvement in identifying survivors, crucial in this context, was due to the effective handling of class imbalance through SMOTE oversampling.
