# audiosepweb
Web app for separating audio using text query

### Running instructions
```bash
git clone https://github.com/pandey-shivani/audiosepweb.git && \
cd audiosepweb && \ 
conda env create -f environment.yml && \
conda activate audiosepweb
```

### Run the API server
```bash
cd backend/
python main.py
```

Visit http://0.0.0.0:8000/docs for API reference


### Run the interface
```bash
cd frontend/
python gradio_interface.py
```

![image](https://github.com/user-attachments/assets/54b18294-4e2a-4c28-8af5-36873d93a07d)



