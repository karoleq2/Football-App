# Football Results Application

A client application designed to analyze and display football results using an SQLite database generated from CSV data.

## How to Run the Project Locally

1. **Clone the repository** to your local machine.
2. **Download the CSV data:** Due to the large size of the dataset, the source CSV files are not stored directly on GitHub. Download the complete data folder from my [Google Drive](https://drive.google.com/drive/folders/1-m_T48cnT_MIFIHb12TsrD9oI1PeUCIH?usp=share_link).
3. **Place the data in the project:** Extract/paste the downloaded `.csv` files into the `static/csv/` directory within the project root.
4. **Build the database:** Run the `setup.py` script. This will read the CSV files and automatically generate the SQLite database inside the `instance/` folder.
5. **Launch the application:** Run `main.py` and open the local address in your web browser.