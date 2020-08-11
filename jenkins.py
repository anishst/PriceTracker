# This is use to run scheduled run in Jenkins
from common.database import Database
import  app

#  code to check latest price
Database.initialize()
app.check_price_selenium()



