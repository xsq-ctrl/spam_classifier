# Dockerfile for spam-classifier project

# 1. 选择一个基础镜像
# 我们选择一个官方提供的、预装了 Miniconda3 的轻量级镜像。
FROM continuumio/miniconda3:4.9.2

# 2. 设置工作目录
# 在容器内部创建一个 /app 目录，并将其设置为后续所有命令的执行目录。
WORKDIR /app

# 3. 复制环境配置文件
# 将宿主机的 environment.yml 文件复制到容器的 /app 目录下。
COPY environment.yml .

# 4. 创建并激活 Conda 环境
# 使用 environment.yml 文件在容器内部创建名为 spam_env 的环境。
# `&& conda clean` 是一个好习惯，可以减小最终镜像的大小。
RUN conda env create -f environment.yml && conda clean -afy

# 5. 设置 Shell 环境
# 告诉 Docker 后续的 SHELL 命令默认在 conda 环境中执行。
# 这使得我们后续可以直接运行 python，而不需要每次都 `conda activate`。
# 单独安装 pip 依赖（确保安装成功）
RUN /opt/conda/envs/spam_env/bin/pip install \
    blinker==1.8.2 \
    click==8.1.8 \
    cramjam==2.11.0 \
    fastparquet==2024.2.0 \
    flask==3.0.3 \
    fsspec==2025.3.0 \
    gunicorn==23.0.0 \
    importlib-metadata==8.5.0 \
    itsdangerous==2.2.0 \
    jinja2==3.1.6 \
    joblib==1.4.2 \
    markupsafe==2.1.5 \
    numpy==1.24.4 \
    packaging==26.0 \
    pandas==2.0.3 \
    psutil==7.2.2 \
    pyarrow==17.0.0 \
    python-dateutil==2.9.0.post0 \
    pytz==2025.2 \
    scikit-learn==1.3.2 \
    scipy==1.10.1 \
    six==1.17.0 \
    threadpoolctl==3.5.0 \
    tzdata==2025.3 \
    werkzeug==3.0.6 \
    zipp==3.20.2

# 设置环境变量
ENV PATH=/opt/conda/envs/spam_env/bin:$PATH

# 6. 复制项目文件
# 将项目根目录下的所有文件（. 表示当前目录）复制到容器的 /app 目录。
# 我们创建一个 .dockerignore 文件来排除不需要复制的内容。
COPY . .

# 7. 设置容器启动时默认执行的命令
# 当容器启动时，默认执行 ./run_training.sh 脚本，并传递 "docker_run" 作为版本号。
RUN mkdir -p data models logs results configs
CMD ["python", "scripts/train.py", "docker_run"]
