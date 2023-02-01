# HUAT API (FLASK)

This Flask API was created to do the following:

* Scrap 4D Results and seed the data
* GET request to return latest result
* GET request to return date of all draws for the past two years
* POST request to check winning number and your prize winnings.
* To be used for a React project

## Set Up

You will require the following to run this locally:

* Latest Python
* PostgreSQL 14.6
* Selenium chromedriver

Will fill in the rest in due time

## API

GET: Retrieve Latest Result

> /api/v1/4d/result
>
> Example Output
>{"draw_date": "Wed, 04 Jan 2023 00:00:00 GMT","draw_number": "4957","first": "2452","second": "4082","third": "6585","starter": "0343,1323,3713,3854,6295,7085,7299,7308,9260,9774","consolation": "0532,0647,3397,3672,5586,5795,7693,7860,8467,8627"}

POST: Check Winning Number

> /api/v1/4d/result
>
> Request body example:
>
>{"drawdate": "18/12/2022","number": ["0184","0349","0367","0184","9420"],"bet": [{"b": 1,"s": 2},{"b": 2,"s": 3},{"b": 3,"s": 4},{"b": 4,"s": 5},{"b": 5,"s": 6}]}
>
> Example output:
>
>{"draw_date":"Sun, 18 Dec 2022 00:00:00 GMT","draw_number":"4950","first":"5139","second":"3115","third":"4040","starter":"0184,0349,0367,3593,6437,6967,7174,7894,8453,9420","consolation":"0343,2114,3502,5573,6184,6643,7781,9099,9462,9645","winningnumber":["starter: 0184, prize: 250","starter: 0349, prize: 500","starter: 0367, prize: 750","starter: 0184, prize: 1000","starter: 9420, prize: 1250"],"totalwinnings":3750}


GET: Retrieve past 2 year draw dates

>/api/v1/4d/dates
>
>Example output:
>
>{"dates":["Wed, 04 Jan 2023 00:00:00 GMT","Sun, 01 Jan 2023 00:00:00 GMT","Sat, 31 Dec 2022 00:00:00 GMT","Wed, 28 Dec 2022 00:00:00 GMT","Sun, 25 Dec 2022 00:00:00 GMT","Sat, 24 Dec 2022 00:00:00 GMT","Wed, 21 Dec 2022 00:00:00 GMT","Sun, 18 Dec 2022 00:00:00 GMT","Sat, 17 Dec 2022 00:00:00 GMT","Wed, 14 Dec 2022 00:00:00 GMT","Sun, 11 Dec 2022 00:00:00 GMT","Sat, 10 Dec 2022 00:00:00 GMT","Wed, 07 Dec 2022 00:00:00 GMT","Sun, 04 Dec 2022 00:00:00 GMT","Sat, 03 Dec 2022 00:00:00 GMT","Wed, 30 Nov 2022 00:00:00 GMT","Sun, 27 Nov 2022 00:00:00 GMT","Sat, 26 Nov 2022 00:00:00 GMT",....
