### Android Emulator Setup

##### Install Android Studio

Check https://developer.android.google.cn/studio/install and follow the instructions.

##### Install Devices and through SdkManager

You can find your Android SDK location through option *File | Settings | Languages & Frameworks | Android SDK* in Android Studio. You need to select a platform with API level=31 in *SDK Platforms* and click *apply*.

Then, you need to add the path to your environment variables.

##### Starting An Emulator

Check https://developer.android.google.cn/studio/run/emulator. Remember to select platform same to our experiment setting when creating new emulator: Choose *small phone*, then select *API 31*.

After starting, you can run following command in command line to check the emulator's id if it runs successfully:

```
adb devices
```

##### Run our program

Replace *<emulator_id>* and *<sdk_path>* with above information in our example command. Congratulations, you can now run with local emulator.
