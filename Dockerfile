# Usa l'ultima immagine ufficiale di Python (attualmente è Python 3.12.x)
FROM python:3.12-slim

#RUN apt-get update && apt-get install -y \
#    curl \
#    ca-certificates \
#    && rm -rf /var/lib/apt/lists/* \
#    && apt-get update -y && apt-get install gringo -y \

# Installa dipendenze di sistema minime per conda
RUN apt-get update && apt-get install -y wget bzip2 && rm -rf /var/lib/apt/lists/*

# Installa Miniconda in /opt/conda
ENV CONDA_DIR=/opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p $CONDA_DIR && \
    rm /tmp/miniconda.sh && \
    $CONDA_DIR/bin/conda clean -afy

# Aggiungi conda al PATH
ENV PATH=$CONDA_DIR/bin:$PATH

RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r


RUN conda install -c potassco -c conda-forge clingo-lp

# Imposta la directory di lavoro dentro il container
WORKDIR /app

# Copia i file del progetto (modifica se necessario)
COPY . /app

# (Opzionale) Installa dipendenze se hai un requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container.
COPY . .
ADD entrypoint.sh entrypoint.sh

RUN chmod -R 777 .

RUN python -m pip install -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 5000

# Run the application.


#CMD nohup python app.py && 


#RUN chmod 777 entrypoint.sh
#CMD nohup streamlit run "CNL ASP Solutions.py" --server.port=8501 --server.address=0.0.0.0 
ENTRYPOINT /app/entrypoint.sh
