from sklearn.model_selection import train_test_split


def join_dataset(ds1, ds2):
    df1.append(df2, ignore_index=True)


def split_dataset(
    features, target, config, train_ratio=0.7, validation_ratio=0.2, test_ratio=0.1
):
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=test_ratio
    )
    X_train, X_validation, y_train, y_validation = train_test_split(
        X_train, y_train, test_size=validation_ratio
    )

    return {
        "features_train": X_train,
        "features_validation": X_validation,
        "features_test": X_test,
        "target_train": y_train,
        "target_validation": y_validation,
        "target_test": y_test,
    }


def get_target(raw_dataset, config):
    return raw_dataset[config["target_name"]].copy()


def drop_target(dataset, config):
    dataset = dataset.drop([config["target_name"]], axis=1)
    return dataset


def subselect_features(dataset, config):
    return dataset[config["feature_list"]]
