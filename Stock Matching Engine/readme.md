

## Matching Engine

A matching engine is a tool used in trading that matches people that want to buy stocks with people that want to sell them. More specifically, it matches buy orders with sell orders; this is called filling an order.
Here is a link if you want more information: https://en.wikipedia.org/wiki/Order_matching_system

1) Creates a new endpoint that takes in "orders" (/orders) and store it in memory. Here is an example data model:
    ```json
    {
        "data":
        {
            "traderId": "skbks-sdk39sd-3ksfl43io3-alkjasf-34",
            "orders":
            [
                {
                    "symbol": "AAPL",
                    "quantity": 100,
                    "orderType": "buy"
                },
                {
                    "symbol": "NVDA",
                    "quantity": 5000,
                    "orderType": "buy"
                },
                {
                    "symbol": "MSFT",
                    "quantity": 2500,
                    "orderType": "sell"
                }
            ]
        }
    }
    ```
   
2) Creates an endpoint to view a given trader's current orders and statuses (/orders/<trader_id>). The data model for that should look something like this:
    ```json
    {
        "data":
        [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "orderType": "buy",
                "orderTime": "2018-10-10 13:30:40.647845",
                "status": "open"
            },
            {
                "symbol": "NVDA",
                "quantity": 5000,
                "orderType": "buy",
                "orderTime": "2018-10-10 13:30:40.647845",
                "status": "open"
            },
            {
                "symbol": "MSFT",
                "quantity": 2500,
                "orderType": "sell",
                "orderTime": "2018-10-10 13:30:40.647845",
                "status": "open"
            }
        ]
    }
    ```
    
3) Matching logic to match buy and sell orders. Here is some sample input/output:

    Trader 1 sends in an order like this:
    ```json
    {
        "data":
        {
            "traderId": "trader1",
            "orders":
            [
                {
                    "symbol": "AAPL",
                    "quantity": 100,
                    "orderType": "buy"
                }
            ]
        }
    }
    ```
    
    Then if you hit `/orders/trader1` it should return:
    ```json
    {
        "data":
        [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "orderType": "buy",
                "orderTime": "2018-10-10 13:30:40.647845",
                "status": "open"
            }
        ]
    }
    ```
    
    And then if Trader 2 sends in something like this:
    ```json
    {
        "data":
        {
            "traderId": "trader2",
            "orders":
            [
                {
                    "symbol": "AAPL",
                    "quantity": 100,
                    "orderType": "sell"
                }
            ]
        }
    }
    ```
    
    and `/orders/trader1` should now look something like this:
    ```json
    {
        "data":
        [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "orderType": "buy",
                "orderTime": "2018-10-10 13:30:40.647845",
                "status": "filled"
            }
        ]
    }
    ```
    
    and `/orders/trader2` should look like this:
    ```json
    {
        "data":
        [
            {
                "symbol": "AAPL",
                "quantity": 100,
                "orderType": "sell",
                "orderTime": "2018-10-10 13:35:40.647845",
                "status": "filled"
            }
        ]
    }
    ```
    
