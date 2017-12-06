# AsyncRobot - RobotFramework

Utility written as PreRunModifier and PostRebotModifier that enables to run Robot tests in a Pause and Play mode

## Getting Started

This is to basically enable running your tests in a Pause and Play mode

For eg.,
Run all the action items and pause on the validation which might take more time or you are testing some batch processing application.
In this case, you can input the previous output.xml generated to ask Robot to start running the tests from where it was paused the next time
you start/resume your execution

Refer to Robot documentation for more info on the modifiers:

http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#programmatic-modification-of-test-data



### Prerequisites
For the tests written using Robot Framework, you can run these scripts as Modifiers while running robot tests to enable running tests in 
a Pause and Play mode

### Installing

Keywords on which you want to pass/stop the execution intermittently need to be mentioned in a flat file in the same working directory as async_keywords.txt
```
Keyword1, Keyword2

```

while running the Robot tests,

```
pybot --prerunmodifier <path_to_file>/PrerunUtility.py:<path to previous output.xml/ None if a fresh execution>
                             --prerebotmodifier PostrunUtility.py  tests/
```

## Authors

* **Bala Kumaran** - *Initial work* - (https://github.com/BalakumaranS)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
