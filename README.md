# MetroScan
MetroScan is a project that utilizes facial recognition technology for automated fare calculation and payment in metro stations. It provides a seamless and convenient experience for metro commuters, allowing them to enter and exit metro stations by having their faces recognized. The fare is calculated accordingly, and users can conveniently pay their balance using the payment link sent through email.

## Features

- Face recognition at entry and exit points of metro stations
- Automated fare calculation
- Payment link sent through email for balance payment
- Integration with MongoDB for storing user data and face encodings
- Email notification for entry and exit events
- User-friendly camera interface for capturing images
- Real-time face detection and recognition using OpenCV and face_recognition libraries

## Project Structure

The project consists of the following main files:

- `fetchdata.py`: Fetches user data and performs face recognition at entry points of metro stations.
- `insertimage.py`: Takes user inputs, captures an image, and saves user data to the MongoDB database.
- `entry.py`/`exit.py`: Performs face recognition at entry/exit points, calculates fare, updates user data, and sends email notifications.

## Getting Started

To run the MetroScan project, follow these steps:

1. Clone the repository: `git clone https://github.com/KunaAl22/MetroScan.git`
2. Set up the necessary API keys in the `keys.py` file.
3. Configure the MongoDB connection by replacing the `mongoKey` variable in each Python file with your MongoDB connection string.
4. Run `fetchdata.py` to perform face recognition at entry points.
5. Run `insertimage.py` to capture user data and save it to the database.
6. Run `exit.py` to perform face recognition at exit points, calculate fare, and send email notifications.


## Dependencies

The project relies on the following dependencies:

- OpenCV: `pip install opencv-python`
- face_recognition: `pip install face-recognition`
- pymongo: `pip install pymongo`
- sendgrid: `pip install sendgrid`

## Contribution

Contributions to MetroScan are welcome! If you have any ideas, suggestions, or bug fixes, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

