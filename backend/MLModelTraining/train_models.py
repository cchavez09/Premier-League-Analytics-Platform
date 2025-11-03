# backend/MLModelTraining/train_models.py
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, f1_score, confusion_matrix
import joblib
import warnings
import json
warnings.filterwarnings('ignore')

class EnsembleModelTrainer:
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data" / "files" / "MLData"
    MODEL_DIR = BASE_DIR / "data" / "files" / "MLModels"

    def __init__(self):
        self.MODEL_DIR.mkdir(parents=True, exist_ok=True)
        self.min_accuracy = 0.90
        self.max_retrain_attempts = 5
        self.max_home_bias = 0.15  # Maximum acceptable difference in home prediction rate

    def load_features(self, feature_type):
        """Load pre-processed features"""
        data_path = self.DATA_DIR / f'{feature_type}_training.csv'
        df = pd.read_csv(data_path)
        print(f"Loaded {feature_type} data: {len(df)} samples, {len(df.columns)} columns")

        # Check class distribution
        class_dist = df['FTR'].value_counts(normalize=True)
        print(f"Class distribution - A: {class_dist.get('A', 0):.2%}, D: {class_dist.get('D', 0):.2%}, H: {class_dist.get('H', 0):.2%}")

        return df

    def check_home_bias(self, y_true, y_pred):
        """Check if model is overfitting to home wins"""
        # Map predictions back to labels
        label_map = {0: 'Away', 1: 'Draw', 2: 'Home'}

        # Calculate prediction distribution
        unique, counts = np.unique(y_pred, return_counts=True)
        pred_dist = dict(zip(unique, counts / len(y_pred)))

        # Calculate actual distribution
        unique_true, counts_true = np.unique(y_true, return_counts=True)
        true_dist = dict(zip(unique_true, counts_true / len(y_true)))

        # Check home win bias
        home_pred_rate = pred_dist.get(2, 0)
        home_true_rate = true_dist.get(2, 0)
        home_bias = home_pred_rate - home_true_rate

        print(f"  Prediction distribution - Away: {pred_dist.get(0, 0):.2%}, Draw: {pred_dist.get(1, 0):.2%}, Home: {pred_dist.get(2, 0):.2%}")
        print(f"  Actual distribution - Away: {true_dist.get(0, 0):.2%}, Draw: {true_dist.get(1, 0):.2%}, Home: {true_dist.get(2, 0):.2%}")
        print(f"  Home bias: {home_bias:+.2%}")

        return abs(home_bias) <= self.max_home_bias

    def prepare_data_splits(self, df, test_size=0.15, val_size=0.15):
        """70-15-15 split with balanced sampling"""
        X = df.drop(columns=['FTR'])
        y = df['FTR'].map({'A': 0, 'D': 1, 'H': 2})

        identifier_cols = ['Date', 'HomeTeam', 'AwayTeam', 'Season', 'TeamID']
        for col in identifier_cols:
            if col in X.columns:
                raise ValueError(f"Identifier column '{col}' found in features! Remove from feature engineering.")

        print(f"Feature columns ({len(X.columns)}): {list(X.columns[:5])}...")

        X = X.fillna(0)
        valid_mask = y.notna()
        X = X[valid_mask]
        y = y[valid_mask]

        # Use stratified split to maintain class balance
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.30, random_state=42, stratify=y
        )

        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        X_test_scaled = scaler.transform(X_test)

        print(f"Split - Train: {len(X_train)} (70%), Val: {len(X_val)} (15%), Test: {len(X_test)} (15%)")

        return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test, scaler, X.columns.tolist()

    def train_with_validation(self, X_train, X_val, y_train, y_val):
        """Train until requirements met using accuracy only"""
        best_accuracy = 0
        best_ensemble = None
        best_params = {}

        for attempt in range(self.max_retrain_attempts):
            print(f"\n--- Attempt {attempt + 1}/{self.max_retrain_attempts} ---")

            # Logistic Regression with balanced class weights
            lr_configs = [
                {'C': 0.01, 'max_iter': 3000, 'class_weight': 'balanced'},
                {'C': 0.1, 'max_iter': 3000, 'class_weight': 'balanced'},
                {'C': 1.0, 'max_iter': 3000, 'class_weight': 'balanced'},
                {'C': 10.0, 'max_iter': 3000, 'class_weight': 'balanced'}
            ]

            best_lr = None
            best_lr_score = 0
            for config in lr_configs:
                lr = LogisticRegression(random_state=42 + attempt, **config)
                lr.fit(X_train, y_train)
                val_pred = lr.predict(X_val)
                score = accuracy_score(y_val, val_pred)
                has_low_bias = self.check_home_bias(y_val, val_pred)

                if score > best_lr_score and has_low_bias:
                    best_lr_score = score
                    best_lr = lr

            print(f"Best LR val accuracy: {best_lr_score:.4f}")

            # KNN
            knn_configs = [
                {'n_neighbors': 7, 'weights': 'distance'},
                {'n_neighbors': 11, 'weights': 'distance'},
                {'n_neighbors': 15, 'weights': 'distance'},
                {'n_neighbors': 21, 'weights': 'distance'}
            ]

            best_knn = None
            best_knn_score = 0
            for config in knn_configs:
                knn = KNeighborsClassifier(**config)
                knn.fit(X_train, y_train)
                val_pred = knn.predict(X_val)
                score = accuracy_score(y_val, val_pred)
                has_low_bias = self.check_home_bias(y_val, val_pred)

                if score > best_knn_score and has_low_bias:
                    best_knn_score = score
                    best_knn = knn

            print(f"Best KNN val accuracy: {best_knn_score:.4f}")

            # SVM with balanced class weights
            svm_configs = [
                {'C': 0.1, 'kernel': 'rbf', 'gamma': 'scale', 'class_weight': 'balanced'},
                {'C': 1.0, 'kernel': 'rbf', 'gamma': 'scale', 'class_weight': 'balanced'},
                {'C': 10.0, 'kernel': 'rbf', 'gamma': 'auto', 'class_weight': 'balanced'},
                {'C': 1.0, 'kernel': 'poly', 'degree': 3, 'class_weight': 'balanced'}
            ]

            best_svm = None
            best_svm_score = 0
            for config in svm_configs:
                svm = SVC(probability=True, random_state=42 + attempt, **config)
                svm.fit(X_train, y_train)
                val_pred = svm.predict(X_val)
                score = accuracy_score(y_val, val_pred)
                has_low_bias = self.check_home_bias(y_val, val_pred)

                if score > best_svm_score and has_low_bias:
                    best_svm_score = score
                    best_svm = svm

            print(f"Best SVM val accuracy: {best_svm_score:.4f}")

            # Ensemble
            ensemble = VotingClassifier(
                estimators=[('lr', best_lr), ('knn', best_knn), ('svm', best_svm)],
                voting='soft'
            )
            ensemble.fit(X_train, y_train)

            val_pred = ensemble.predict(X_val)
            val_accuracy = accuracy_score(y_val, val_pred)

            print(f"\nEnsemble validation results:")
            print(f"  Accuracy: {val_accuracy:.4f}")
            has_low_bias = self.check_home_bias(y_val, val_pred)

            if has_low_bias and val_accuracy > best_accuracy:
                best_accuracy = val_accuracy
                best_ensemble = ensemble
                best_params = {
                    'lr_params': best_lr.get_params(),
                    'knn_params': best_knn.get_params(),
                    'svm_params': best_svm.get_params(),
                    'val_accuracy': float(val_accuracy),
                    'attempt': attempt + 1,
                    'has_low_home_bias': True
                }

            if val_accuracy >= self.min_accuracy and has_low_bias:
                print(f"\n✓ Requirements met! Accuracy: {val_accuracy:.4f}, Low home bias")
                break

        if best_accuracy < self.min_accuracy:
            print(f"\n⚠ Warning: Best model below requirements")
            print(f"  Accuracy: {best_accuracy:.4f} (need {self.min_accuracy})")

        return best_ensemble, best_params

    def train_model(self, model_name):
        """Train a single model type"""
        print(f"\n{'='*70}")
        print(f"=== Training {model_name.title()} Model ===")
        print(f"{'='*70}")

        df = self.load_features(model_name)
        X_train, X_val, X_test, y_train, y_val, y_test, scaler, features = self.prepare_data_splits(df)

        ensemble, params = self.train_with_validation(X_train, X_val, y_train, y_val)

        print("\n--- Test Set Evaluation ---")
        test_pred = ensemble.predict(X_test)
        test_acc = accuracy_score(y_test, test_pred)
        test_f1 = f1_score(y_test, test_pred, average='weighted')

        print(f"Test Accuracy: {test_acc:.4f}")
        print(f"Test F1: {test_f1:.4f}")

        # Check test set home bias
        print("\nTest set bias check:")
        self.check_home_bias(y_test, test_pred)

        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, test_pred)
        print("           Predicted")
        print("         A    D    H")
        print(f"Actual A {cm[0][0]:4d} {cm[0][1]:4d} {cm[0][2]:4d}")
        print(f"       D {cm[1][0]:4d} {cm[1][1]:4d} {cm[1][2]:4d}")
        print(f"       H {cm[2][0]:4d} {cm[2][1]:4d} {cm[2][2]:4d}")

        print("\n" + classification_report(y_test, test_pred, target_names=['Away', 'Draw', 'Home']))

        # Save models
        model_path = self.MODEL_DIR / f'{model_name}_ensemble.pkl'
        scaler_path = self.MODEL_DIR / f'{model_name}_scaler.pkl'
        features_path = self.MODEL_DIR / f'{model_name}_features.pkl'
        params_path = self.MODEL_DIR / f'{model_name}_params.json'

        joblib.dump(ensemble, model_path)
        joblib.dump(scaler, scaler_path)
        joblib.dump(features, features_path)

        params['test_accuracy'] = float(test_acc)
        params['test_f1_score'] = float(test_f1)
        params['num_features'] = len(features)

        with open(params_path, 'w') as f:
            json.dump(params, f, indent=2)

        print(f"\n✓ Saved to {self.MODEL_DIR}/")

    def train_all_models(self):
        """Train both models"""
        self.train_model('current_season')
        self.train_model('historical')

        print(f"\n{'='*70}")
        print("✓ All models trained successfully!")
        print(f"{'='*70}")

if __name__ == "__main__":
    trainer = EnsembleModelTrainer()
    trainer.train_all_models()