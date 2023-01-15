# YURfit-api
API wrapper for the unofficial YUR Fit API

## Usage
Clone the repo and create a new file inside it with the following content:
```python
import YURfitAPI

yur = YURfitAPI.YURfitAPI("your key")
yur.login("email", "password")
yur.getAccountInfo()

print(yur.getWorkouts())
```
I have no idea you can get the key without encrypting the HTTPS traffic from your smartphone and read it out from there -> TODO!