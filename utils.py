import os
import streamlit as st

def list_files_in_directory(directory):
    files = os.listdir(directory)
    return files

def main():
    st.title("List Files in Directory")
    
    # Sidebar input for directory path
    directory_path = "saved_models"
    
    # Display files in the directory
    files = list_files_in_directory(directory_path)
    
    st.write(f"Files in {directory_path}:")
    
    for file in files:
        # Display download link for each file
        file_path = os.path.join(directory_path, file)
        st.write(f"[{file}]({file_path})")
        with open()
        st.download_button("download", file_name=file)
    
if __name__ == "__main__":
    main()
