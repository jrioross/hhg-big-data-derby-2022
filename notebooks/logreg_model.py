import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
import mlflow


def model_template(df, 
                   target,
                   categorical_cols
                   ):

    # this first line assumes we ran the following in command line:
    # mlflow ui --backend-store-uri sqlite:///mlflow.db
    # which uses MLflow Local run using SQLite for backen storage (mlflow.db)
    mlflow.set_tracking_uri("sqlite:///mlflow.db")

    # this line sets the experiment under which our models will be recorded
    mlflow.set_experiment("big-derby-2022")

    with mlflow.start_run(run_name="Run logreg"):
    # split data into features (X) and target (y)
        X = df.drop(columns = target)
        y = df['target']

        # now split the data set into a training set and a test set
        X_train, X_test, y_train, y_test = train_test_split(X, 
                                                            y, 
                                                            test_size = 0.2,  # Let's let 20% of the data be used for testing
                                                            random_state = 42, # We can fix a random state for a reproducible split. The one we choose can be arbitrary.
                                                            stratify = target # Stratification, while unnecessary, is useful. It ensures that, if you're target is classifications, train and test have roughly equal proportions to each other (and to the original set).
                                                            )

        # one-hot encode categorical values, i.e., transform the data so that categorical variables get one column for each category, with ones and zeros filling those columns.
        # we put the one-hot encoder into a ColumnTransformer pipeline to help us more easily manage what to do with which parts of the data.
        ohe = OneHotEncoder(drop = 'first', handle_unknown='ignore')
        ct = ColumnTransformer(
            [("ohe", ohe)],
            columns = categorical_cols,
            remainder='passthrough'
        )

        # let's also assume here that we want to put all of our numerical columns on the same scale. StandardScaler converts numerical columns to Z-scores.
        scaler = StandardScaler()

        # we also need to instantiate our logistic regression model. these can be customized and "tuned", but we'll get into that later. (notice in the docs that the default "penalty" is a mysterious "l2".)
        logreg = LogisticRegression()

        # we have several steps here. now we compose them all together in a single pipeline, which takes a list of tuples of the form ("name", step), much like the ColumnTransformer.
        pipe = Pipeline(
            [
                ("ct", ct),
                ("scaler", scaler),
                ("logreg", logreg)
            ]
        )

        # after we build the pipeline, we "run it" with the fit_transform() method, which transforms the data and fits the model to the data, as appropriate.
        # note that we fit_transform() on the training data. also note that no assignment is necessary. the transformations and fit are under the hood.
        pipe.fit_transform(X_train, y_train)

        # now that we have built a pipeline for handling data and trained a model on our training data, we use the model to predict values in with our test data.
        # note that y_test does NOT go in here. we use y_test to check our model's performance.
        y_preds = pipe.predict(X_test)

        # so, let's check that performance. if our model is a classifier, as we presumed here, then we can use some nifty tools provided in sklearn.
        # tool 1: confusion matrix
        # tool 2: classification report
        # more tools: specific evaluation values like f1_score, accuracy, precision, and recall
        cm = confusion_matrix(y_test, y_preds)
        report = classification_report(y_test, y_preds)

    return cm, report