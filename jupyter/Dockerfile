FROM bitnami/spark:3.5.6

USER root

# 设置时区为上海和中文环境
ENV TZ=Asia/Shanghai
ENV LANG=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 使用国内镜像源
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 安装系统依赖和中文语言支持
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    wget \
    curl \
    vim \
    git \
    procps \
    locales \
    fontconfig \
    fonts-wqy-microhei \
    fonts-wqy-zenhei \
    ttf-wqy-zenhei \
    && rm -rf /var/lib/apt/lists/* \
    && echo "zh_CN.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen zh_CN.UTF-8

# 设置pip使用国内镜像
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装Jupyter Notebook和常用数据科学库
RUN pip3 install --no-cache-dir \
    jupyter \
    jupyterlab \
    jupyterlab-language-pack-zh-CN \
    notebook \
    ipykernel \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    scikit-learn \
    scipy \
    pyspark==3.5.6 \
    mysql-connector-python \
    pyhdfs \
    hdfs \
    findspark \
    requests \
    beautifulsoup4 \
    lxml

# 配置matplotlib中文字体
# 创建matplotlib配置文件设置中文字体
RUN mkdir -p /home/jovyan/.config/matplotlib && \
    echo "font.family: sans-serif" >> /home/jovyan/.config/matplotlib/matplotlibrc && \
    echo "font.sans-serif: WenQuanYi Micro Hei, WenQuanYi Zen Hei, DejaVu Sans, Liberation Sans, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, sans-serif" >> /home/jovyan/.config/matplotlib/matplotlibrc && \
    echo "axes.unicode_minus: False" >> /home/jovyan/.config/matplotlib/matplotlibrc && \
    echo "# 中文字体设置" >> /home/jovyan/.config/matplotlib/matplotlibrc && \
    echo "font.size: 10.0" >> /home/jovyan/.config/matplotlib/matplotlibrc

# 创建Jupyter Notebook的matplotlib默认配置
RUN mkdir -p /home/jovyan/.ipython/profile_default/ && \
    echo "c = get_config()" >> /home/jovyan/.ipython/profile_default/ipython_config.py && \
    echo "c.InteractiveShellApp.matplotlib = 'inline'" >> /home/jovyan/.ipython/profile_default/ipython_config.py && \
    echo "c.InlineBackend.figure_format = 'retina'" >> /home/jovyan/.ipython/profile_default/ipython_config.py

# 复制MySQL JDBC驱动
COPY mysql-connector-java-8.0.32.jar /opt/bitnami/spark/jars/mysql-connector-java.jar

# 修复Spark权限问题
RUN mkdir -p /opt/bitnami/spark/tmp && chmod 777 /opt/bitnami/spark/tmp

# 创建Jupyter用户和目录
RUN useradd -m -s /bin/bash jovyan && \
    mkdir -p /home/jovyan/work && \
    mkdir -p /home/jovyan/.local/share/jupyter && \
    chown -R jovyan:jovyan /home/jovyan

# 配置Jupyter
RUN mkdir -p /home/jovyan/.jupyter && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> /home/jovyan/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.port = 8888" >> /home/jovyan/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> /home/jovyan/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.token = ''" >> /home/jovyan/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> /home/jovyan/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> /home/jovyan/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.notebook_dir = '/home/jovyan/work'" >> /home/jovyan/.jupyter/jupyter_notebook_config.py

# 配置Spark环境变量
ENV SPARK_HOME=/opt/bitnami/spark
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV PYTHONPATH=/opt/bitnami/spark/python:/opt/bitnami/spark/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
ENV PATH=$SPARK_HOME/bin:$PATH
ENV JUPYTERLAB_LANG=zh_CN

# 创建IPython启动脚本，确保中文字体加载
RUN mkdir -p /home/jovyan/.ipython/profile_default/startup && \
    echo 'import matplotlib' > /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo 'import matplotlib.font_manager as fm' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo 'import os' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo 'font_paths = [' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo "    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'," >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo "    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'," >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo ']' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo 'for fp in font_paths:' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo '    if os.path.exists(fp):' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo '        fm.fontManager.addfont(fp)' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo '        print(f\"Added font: {fp}\")' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo '    else:' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo '        print(f\"Font not found: {fp}\")' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo '# 设置rcParams' >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo "matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei'] + matplotlib.rcParams['font.sans-serif']" >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo "matplotlib.rcParams['font.family'] = 'sans-serif'" >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    echo "matplotlib.rcParams['axes.unicode_minus'] = False" >> /home/jovyan/.ipython/profile_default/startup/00-matplotlib-fonts.py && \
    chown -R jovyan:jovyan /home/jovyan/.ipython

# 复制Hadoop配置文件（从宿主机挂载）
RUN mkdir -p /opt/hadoop/etc/hadoop

# 切换用户
USER jovyan

# 设置工作目录
WORKDIR /home/jovyan/work

# 启动Jupyter Notebook
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]