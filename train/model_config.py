from scipy.stats import randint, uniform

LIGHTGBM_PARAMS = {
    'n_estimators': randint(500, 1500),         
    'max_depth': randint(5, 15),                
    'learning_rate': uniform(0.01, 0.05),       
    'num_leaves': randint(20, 50),              
    'min_child_samples': randint(50, 200),      
    'reg_alpha': uniform(0, 10),                
    'reg_lambda': uniform(0, 10),               
    'boosting_type': ['gbdt', 'dart']           
}

RANDOM_SEARCH_PARAMS = {
    'n_iter': 15,                               
    'cv': 5,                                    
    'n_jobs': -1,
    'verbose': 2,
    'random_state': 42,
    'scoring': 'neg_root_mean_squared_error'     
}