# How to run the application

1. Open the terminal in the folder where you downloaded the application to.


2. If on Mac or linux then we need to make the script executable. Run 'chmod +x run.sh'. This will make sure you can run the script.

```
chmod +x run.sh
```

3. Run the actual run.sh script on Mac or Linux, run.ps1 on Windows.
```
./run.sh
```
```
./run.ps1
```

## Commands
Display help
```
help
```

Create a heatmap
```
heatmap -b [bodypart]

```
If you would want a heatmap of the centre of the body:
```
heatmap -b centre
```

Create a trace of followed path
```
trace -b [bodypath]
```
If you would want a trace of the centre of the body:
```
trace -b centre
```
Creating a csv file for the inputfiles with the distance and speed per time interval.

```
dist_interval_csv -b [Bodypart] -s [Size] -t [Timeinterval]
```

Results: Speed is in cm per second, distance is in cm.

Arguments: Size (-s) is in cm. Time interval (-t) is in seconds. Bodypart (-b) is the bodypart used

```
dist_interval_csv -b centre -s 50x50 -t 120
```