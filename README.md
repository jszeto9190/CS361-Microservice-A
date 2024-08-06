# CS361-Microservice-A: Image Generator Microservice
This microservice allows you to generate and download images based on a user-defined search term. It uses the Google Custom Search API to find images and then provides endpoints to generate images, view logs, and download images.

## How to Request Data
1. Download user-app.py and save it to the folder location of your choice.
2. Ensure you download all necessary modules and run Python 3.6 or higher.
3. Scroll down to __main__ in user-app.py.
4. Modify text, save_directory, and num_images in user-app.py.
   - text: Designated image search term.
   - save_directory: Folder name that you would like to save the images. This folder will appear in the same folder as the location of user-app.py.
   - num_images: The number of images that you want to generate.
  For example:
    ```
    text = "oregon state university" # MODIFY THIS SEARCH TERM
    save_directory = "Pictures" # MODIFY THIS FILE NAME
    num_images = 2 # MODIFY THIS IMAGE AMOUNT (MAX 10 IMAGES)
    ```
5. Run the following code in the terminal where the folder holding user-app.py is located.
   ```
   python user-app.py
   ```
## How to Receive Data
1. Image source URL and file location data are stored under response_data. This information is also printed in the terminal. 
   ![image](https://github.com/user-attachments/assets/e50704ae-d13c-4b0c-8737-c0ce527220bd)
   
   The generated images will appear in the save_directory folder.  
   ![image](https://github.com/user-attachments/assets/31269445-2e1c-4d0d-b2d8-8ff31b399783)  


## How to View Logs
You may want to understand what is happening on the backend of the microservice. If so, visit https://microservice-a-cs361-c3c3bdb288e7.herokuapp.com/ and select 'View Logs'.

## UML Sequence Diagram
![UML Sequence Diagram](https://github.com/user-attachments/assets/353948dd-5a9a-4a43-988f-0e549bc8ad28)
