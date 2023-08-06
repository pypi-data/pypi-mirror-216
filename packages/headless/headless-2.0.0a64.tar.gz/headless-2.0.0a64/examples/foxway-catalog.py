# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio

from headless.ext.foxway import FoxwayClient
from headless.ext.foxway.v1 import PricelistProduct


async def main():
    async with FoxwayClient() as client:
        params: dict[str, str] = {
            'dimensionGroupId': '11',
            'itemGroupId': '12',
            'vatMargin': 'false'
        }
        async for dto in client.listall(PricelistProduct, 'working', params=params):
            print(dto.item_variant_id, dto.sku, dto.product_name, dto.price, dto.quantity)
            for dimension in dto.dimension:
                print(f'- {dimension.key}: {dimension.value}')

if __name__ == '__main__':
    asyncio.run(main())