from pandas import DataFrame
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import io

from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression



def get_categorical_cols(dataset: DataFrame) -> list:
    obj = dataset.dtypes == "object"
    object_cols = list(obj[obj].index)
    print("Categorical variables:", len(object_cols))
    return object_cols


def get_numerical_cols(dataset) -> list:
    int_ = dataset.dtypes == "int"
    num_cols = list(int_[int_].index)
    print("Numerical variables:", len(num_cols))
    return num_cols


def get_float_cols(dataset) -> list:
    fl = dataset.dtypes == "float"
    fl_cols = list(fl[fl].index)
    print("Float variables:", len(fl_cols))
    return fl_cols


def create_heatmap(numerical_dataset):
    plt.figure(figsize=(12, 6))
    sns.heatmap(
        numerical_dataset.corr(), cmap="BrBG", fmt=".2f", linewidths=2, annot=True
    )
    plt.savefig("correlation_heatmap.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_barplot(object_cols: list, dataset: DataFrame):
    unique_values = []
    for col in object_cols:
        unique_values.append(dataset[col].unique().size)
    plt.figure(figsize=(10, 6))
    plt.title("No. Unique values of Categorical Features")
    plt.xticks(rotation=90)
    sns.barplot(x=object_cols, y=unique_values)
    plt.savefig("categorical_unique_values.png", dpi=300, bbox_inches="tight")
    plt.close()


def create_complex_barplot(object_cols: list, dataset: DataFrame):
    plt.figure(figsize=(18, 36))
    plt.title("Categorical Features: Distribution")
    plt.xticks(rotation=90)
    index = 1

    for col in object_cols:
        y = dataset[col].value_counts()
        plt.subplot(11, 4, index)
        plt.xticks(rotation=90)
        sns.barplot(x=list(y.index), y=y)
        index += 1

    plt.savefig("categorical_features_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()


def process(pdfFile: bytes):
    dataset = pd.read_excel(io.BytesIO(pdfFile))
    print(dataset.head(5))
    print(dataset.shape)

    object_cols = get_categorical_cols(dataset)
    numerical_cols = get_numerical_cols(dataset)
    float_cols = get_float_cols(dataset)
    numerical_dataset = dataset.select_dtypes(include=["number"])

    create_heatmap(numerical_dataset)
    create_barplot(object_cols, dataset)
    create_complex_barplot(object_cols, dataset)

    dataset.drop(["Id"], axis=1, inplace=True)
    dataset["SalePrice"] = dataset["SalePrice"].fillna(dataset["SalePrice"].mean())
    new_dataset = dataset.dropna()
    s = new_dataset.dtypes == "object"
    object_cols = list(s[s].index)
    OH_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    OH_cols = pd.DataFrame(OH_encoder.fit_transform(new_dataset[object_cols]))
    OH_cols.index = new_dataset.index
    OH_cols.columns = OH_encoder.get_feature_names_out()
    df_final = new_dataset.drop(object_cols, axis=1)
    df_final = pd.concat([df_final, OH_cols], axis=1)
    X = df_final.drop(["SalePrice"], axis=1)
    Y = df_final["SalePrice"]

    X_train, X_valid, Y_train, Y_valid = train_test_split(
        X, Y, train_size=0.8, test_size=0.2, random_state=0
    )

    model_SVR = svm.SVR()
    model_SVR.fit(X_train, Y_train)
    Y_pred = model_SVR.predict(X_valid)
    print(mean_absolute_percentage_error(Y_valid, Y_pred))

    model_RFR = RandomForestRegressor(n_estimators=10)
    model_RFR.fit(X_train, Y_train)
    Y_pred = model_RFR.predict(X_valid)
    print(mean_absolute_percentage_error(Y_valid, Y_pred))

    model_LR = LinearRegression()
    model_LR.fit(X_train, Y_train)
    Y_pred = model_LR.predict(X_valid)
    print(mean_absolute_percentage_error(Y_valid, Y_pred))