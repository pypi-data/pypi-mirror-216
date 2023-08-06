
# MoneyKit Python Library

[![pypi](https://img.shields.io/pypi/v/fern-moneykit.svg)](https://pypi.python.org/pypi/fern-moneykit)
[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)

## Installation

Add this dependency to your project's build file:

```bash
pip install fern-moneykit
# or
poetry add fern-moneykit
```

## Usage

```python
from moneykit.client import MoneyKit
from moneykit import LinkSessionCustomerUser

moneykit_client = MoneyKit(token="API_TOKEN")

token_response = moneykit_client.link_session.create_link_session(
  customer_user=LinkSessionCustomerUser(
    id="user_uuid", 
  ),
  webhook="https://url/to/my/webhook",
);

print(token_response)
```

## Async Client

```python
from moneykit.client import AsyncMoneyKit
from moneykit import LinkSessionCustomerUser

import asyncio

moneykit_client = AsyncMoneyKit(token="API_TOKEN")

async def create_link_session() -> None:
    token_response = moneykit_client.link_session.create_link_session(
      customer_user=LinkSessionCustomerUser(
        id="user_uuid", 
      ),
      webhook="https://url/to/my/webhook",
    );
    print(token_response)

asyncio.run(create_link_session())
```

## Sandbox Environment
By default, the client will use the Production Environment. Below is an example of how you can specify using the Sandbox Environment:

```python
from moneykit.client import MoneyKit
from moneykit.environment import MoneyKitEnvironment

sandbox_client = MoneyKit(environment=MoneyKitEnvironment.SANDBOX, token="API_TOKEN")
```

## Handling Exceptions
All exceptions thrown by the SDK will sublcass [moneykit.ApiError](./src/moneykit/core/api_error.py). 

```python
from moneykit.core import ApiError
from moneykit import BadRequestError

try:
  moneykit_client.institutions.get_institution(institution_id='my_id')
except BadRequestError as e: 
  # handle bad request error
except APIError as e:  
  # handle any api related error
```

Error codes are as followed:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `UnauthorizedError`        |
| 403         | `ForbiddenError`           |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `TooManyRequestsError`     |

## Beta status

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning the package version to a specific version in your pyproject.toml file. This way, you can install the same version each time without breaking changes unless you are intentionally looking for the latest version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
