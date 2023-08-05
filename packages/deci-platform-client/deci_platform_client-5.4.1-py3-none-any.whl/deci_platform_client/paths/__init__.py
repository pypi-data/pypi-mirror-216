# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from deci_platform_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    VERSION = "/version"
    HEALTHZ = "/healthz"
    AUTONAC_MODEL_NAME_FILE_NAME = "/autonac/{model_name}/{file_name}"
    COMPANIES_STATS = "/companies/stats"
    CONVERSION_MODEL_ID = "/conversion/{model_id}"
    EVENTS_UPGRADE = "/events/upgrade"
    EVENTS_SUPPORT = "/events/support"
    EVENTS_BUYMODEL = "/events/buy-model"
    EVENTS_REQUESTMODEL = "/events/request-model"
    EVENTS_COMPAREMODELSINMODELZOO = "/events/compare-models-in-model-zoo"
    EVENTS_REQUESTPUBLICARCHITECTURE = "/events/request-public-architecture"
    EVENTS_QUOTAINCREASE = "/events/quota-increase"
    EVENTS_TYPE = "/events/{type}"
    EVENTS_ = "/events/"
    EXPERIMENTS_ = "/experiments/"
    EXPERIMENTS_EXPERIMENT_ID_UPLOAD_URL = "/experiments/{experiment_id}/upload_url"
    EXPERIMENTS_COUNTER = "/experiments/counter"
    GLOBALCONFIGURATION_HARDWARE = "/global-configuration/hardware"
    GLOBALCONFIGURATION_HARDWARETYPES = "/global-configuration/hardware-types"
    GLOBALCONFIGURATION_FRAMEWORKS = "/global-configuration/frameworks"
    GLOBALCONFIGURATION_ARCHITECTURES = "/global-configuration/architectures"
    GLOBALCONFIGURATION_DEEPLEARNINGTASKS = "/global-configuration/deep-learning-tasks"
    GLOBALCONFIGURATION_PERFORMANCEMETRICS = "/global-configuration/performance-metrics"
    GLOBALCONFIGURATION_ACCURACYMETRICS = "/global-configuration/accuracy-metrics"
    GLOBALCONFIGURATION_BATCHSIZES = "/global-configuration/batch-sizes"
    GLOBALCONFIGURATION_QUANTIZATIONLEVELS = "/global-configuration/quantization-levels"
    GLOBALCONFIGURATION_FEATUREFLAGS = "/global-configuration/feature-flags"
    INVITES_ = "/invites/"
    MODELREPOSITORY_MODELS = "/model-repository/models"
    MODELREPOSITORY_MODELS_NAME_NAME = "/model-repository/models/name/{name}"
    MODELREPOSITORY_MODELS_MODEL_ID = "/model-repository/models/{model_id}"
    MODELREPOSITORY_MODELS_VERIFY_NAME = "/model-repository/models/verify/name"
    MODELREPOSITORY_MODELS_VERIFY = "/model-repository/models/verify"
    MODELREPOSITORY_V2_MODELS = "/model-repository/v2/models"
    MODELREPOSITORY_MODELS_PUBLIC = "/model-repository/models/public"
    MODELREPOSITORY_MODELS_MODEL_ID_OPTIMIZED = "/model-repository/models/{model_id}/optimized"
    MODELREPOSITORY_MODELS_BENCHMARK_BENCHMARK_REQUEST_ID = "/model-repository/models/benchmark/{benchmark_request_id}"
    MODELREPOSITORY_MODELS_MODEL_ID_BENCHMARK = "/model-repository/models/{model_id}/benchmark"
    MODELREPOSITORY_MODELS_MODEL_ID_OPTIMIZED_MODELS = "/model-repository/models/{model_id}/optimized_models"
    MODELREPOSITORY_MODELS_MODEL_ID_AUTONAC = "/model-repository/models/{model_id}/autonac"
    MODELREPOSITORY_MODELS_MODEL_ID_OPTIMIZE = "/model-repository/models/{model_id}/optimize"
    MODELREPOSITORY_MODELS_MODEL_ID_GRU = "/model-repository/models/{model_id}/gru"
    MODELREPOSITORY_MODELS_MODEL_NAME_UPLOADURL = "/model-repository/models/{model_name}/upload-url"
    MODELREPOSITORY_MODELS_MODEL_NAME_COPYFILE = "/model-repository/models/{model_name}/copy-file"
    MODELREPOSITORY_MODELS_MODEL_ID_DOWNLOADURL = "/model-repository/models/{model_id}/download-url"
    MODELREPOSITORY_MODELS_MODEL_ID_DEPLOY_INFERY = "/model-repository/models/{model_id}/deploy/infery"
    MODELREPOSITORY_MODELZOO = "/model-repository/model-zoo"
    SNIPPETS_TEMPLATE_NAME = "/snippets/template/{name}"
    SUPPORT_LOG = "/support/log"
    SUPPORT_UPLOADLOGURL = "/support/upload-log-url"
    USERS_ = "/users/"
    USERS_USER_ID = "/users/{user_id}"
    USERS_USER_ID_ACTIVITY = "/users/{user_id}/activity"
    WORKSPACES_STATS = "/workspaces/stats"
    WORKSPACES_ = "/workspaces/"
    WORKSPACES_ID = "/workspaces/{id}"
    WORKSPACES_WORKSPACE_ID_MEMBERS = "/workspaces/{workspace_id}/members"
    ARCHITECTURES = "/architectures"
    ARCHITECTURES_USER = "/architectures/user"
