run:
	venv\Scripts\activate &&  streamlit run chatbot.py


updatedb:
	venv\Scripts\activate && cd vectorDB && python make_faiss_db.py