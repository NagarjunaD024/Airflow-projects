import typing
import tea_pot


def get_provider_info() -> typing.Dict[str,typing.Any]:
    return {
        "package-name": "airflow-provider-tea-pot",  # Required
        "name": "Tea Pot",  # Required
        "description": "custom distribution",  # Required
        "versions": airflow_provider_tea_pot.__version__,  # Required
        "connection-types" : [
             {
                "connection-type": "teapot",
                "hook-class-name": "tea_pot.hooks.TeaPotHook"
            }
        ]
    }
