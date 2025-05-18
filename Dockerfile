# Utiliser une image de base Python
FROM ubuntu:20.04

# Définir les arguments pour les versions de Python et Terraform
ARG PYTHON_VERSION
ARG TERRAFORM_VERSION

# Mettre à jour les paquets et installer les dépendances
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Installer Terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Installer pip
RUN apt-get update && apt-get install -y python3-pip

# Installer yamllint
RUN pip install yamllint

# Installer task
RUN wget https://github.com/go-task/task/releases/download/v3.33.0/task_linux_amd64.tar.gz && \
    tar xzvf task_linux_amd64.tar.gz && \
    mv task /usr/local/bin/ && \
    rm task_linux_amd64.tar.gz

# Vérifier les installations
RUN python3 --version
RUN terraform --version
RUN yamllint --version
RUN task --version

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de votre application
COPY . .

# Installer les dépendances Python (si vous en avez)
# RUN pip install -r requirements.txt

# Commande par défaut (si nécessaire)
# CMD ["votre-commande"]