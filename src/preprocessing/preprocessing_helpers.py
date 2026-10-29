# This function takes x_train & x_test after splitting and makes rare-category 
# grouping for columns with categories > 5 according to x_train only to prevent data leakage
def group_rare_categories(X_train, X_test, threshold=0.05, min_categories=5):
    X_train = X_train.copy()
    X_test = X_test.copy()
    
    categorical_cols = X_train.select_dtypes(include=['object', 'category']).columns
    
    for col in categorical_cols:
        if X_train[col].nunique() > min_categories:
            proportions = X_train[col].value_counts(normalize=True)
            frequent_cats = proportions[proportions >= threshold].index.tolist()
            
            X_train[col] = X_train[col].apply(lambda val: val if val in frequent_cats else 'Other')
            X_test[col] = X_test[col].apply(lambda val: val if val in frequent_cats else 'Other')
            
    return X_train, X_test 

# This function takes a list of (Numeric) columns that needs to be clipped after splitting
def clip_selected_columns(x_train, x_test, columns_to_clip, lower=0.01, upper=0.99):
    X_train = x_train.copy()
    X_test = x_test.copy()
    
    for col in columns_to_clip:
        lower_bound = X_train[col].quantile(lower)
        upper_bound = X_train[col].quantile(upper)
        
        X_train[col] = X_train[col].clip(lower=lower_bound, upper=upper_bound)
        X_test[col] = X_test[col].clip(lower=lower_bound, upper=upper_bound)
        
    return X_train, X_test