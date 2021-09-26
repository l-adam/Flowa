# [Flowa](https://flowa.netlify.app)
## The Mapping Platform for Displaying Flow Data

### What Is Flowa?
Flowa is an experimental mapping platform with an easy-to-navigate interface and exceptional performance. In its current state it’s a demo of how it could be used to present the spread of the virus over a period of time.

### Web Application Structure
- Home page
- Map
- Statistics
- Contribute
- Support
- About Us

The only fully functional part of the website is the map. The rest is for illustration purposes only and therefore is not functional.

### Map Features
- Fully dynamic fetching 
- Decoupled from the backend (the map’s operation is set only by a configuration file on the backend)
- Supports ZIP compression natively
- Supports both poly-based and point-based sources of data
- Supports displaying multiple data overlays at the same time
- Timeline feature integrated with dynamic data fetching and month-by-month statistics
- Search function
- Mouse and touch support
- Fast loading times
- Tested on all major browsers

### Map Generation Scripts
There are some sample data processing scripts included. Based on how they were constructed one can learn how to generate GeoJSON files in Python and how to drastically reduce their size utilizing a cascaded-union optimization algorithm and ZIP compression.

### How test the website locally
#### Mac & Linux
Go to the main project directory in Terminal and execute `./simpleServer.sh`. Press `Ctrl+C` on the keyboard to finish.

#### Windows
Go to the main project directory in CMD and execute `python -m SimpleHTTPServer 8888`. Press `Ctrl+C` on the keyboard to finish.

### Additional Notes
The website is not optimized for smartphones. There are no technical limitations regarding smartphone support — only the layout has to be optimized.

### Performance
Raw GeoJSON data is extremely unoptimized. In the case of the included demo each map data source was taking up about 14.8 MB and there were 28 of them, two for each month. Hundreds of megabytes of assets resulted in abysmal performance even for such a simple demo. Optimizations on the data processing side (cascaded_union algorithm) resulted in a decrease to about 0.6 MB and compression brought it down even further to just about 0.015 MB per data source.

Additionally, the front end side takes advantage of the asynchronous nature of JavaScript to improve the performance even further. All of the above results in near instantaneous loading times — down from about 30 seconds per source which was the case before optimizations.