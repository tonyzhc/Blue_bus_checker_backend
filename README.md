# Blue_bus_checker_backend
Makeathon 2/9/2019

Backend api for connecting to the Alexa skill demo Blue bus checker, a voice assistant program that tells you when the next blue bus is arriving.
Note: this is a demo made in 24 hours during a makeathon event.
- Used chalice to deploy the backend to AWS lambda
- Used google map api to access the estimation of walking time to the bus stop to provide better experience
- Will calculate time and tell user to catch the second next bus if the current one is not working
- Thank you to John Dixon for providing us the library https://github.com/dixonaws/simple-aws-restful-api
