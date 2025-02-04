# From Code to Kubernetes: Deploying a Containerised Application on AKS

When working with Azure, setting up the right environment is the first step toward managing your applications effectively. 

In this guide, we'll walk through the process of creating: 
<ul>
    <li><strong>Resource Group</strong></li>
    <li><strong>Virtual Machine (VM)</strong></li>
    <li><strong>Clone the repository</strong></li>
    <li><strong>Building a Docker image</strong></li>
    <li><strong>Push Image to an Azure Container Registry (ACR)</strong></li>
    <li><strong>Deploy Image Azure Kubernetes Service (AKS)</strong></li>
</ul>

## Prerequisites
- An active Azure account.

## Create a Resource Group
A resource group is a container for managing your Azure resources. A resource group is essential because deleting a resources group will delete all the resources( eg, VM, cluster), all at once, instead of deleting them individually yourself. To create a new resource group, follow the steps below.

Go to your **Azure portal** and in the search bar, type **resource** and click on the first one.

![Resouce -group](images/from-code-to-k8s-images/images/resource-group.png)


Now click on **Create**

![Resouce -group](images/from-code-to-k8s-images/images/click-on-create.png)

Provide your **Resource group** name as shown below:

![Resouce -group](images/from-code-to-k8s-images/images/name-of-resource-group.png)

Click on the **``Next : Tags``** button below which will take you to the tag page. Add a tag as shown below:
**Note**
    Tagging your resources is important for tracking usage and managing costs across different environments effectively. 

![Resouce -group](images/from-code-to-k8s-images/images/resource-tag.png)

Then click on the **``Next:Review + create``** button, which will take you to the page shown below:

![Resouce -group](images/from-code-to-k8s-images/images/resource-review.png)

And finally, Click **``Create``**. This will create your resource group.

![Resouce -group](images/from-code-to-k8s-images/images/resource-group-created.png)

Well done! Your **resource group** has succussfully been created. Now, let's move on to the next stage.

## Create a Virtual Machine(VM)
### 1. Setting up
Now, we will create a VM within our resource group. In this VM we will install and configure **``kubectl``**, so we can communicate with the K8s cluter from the **CLI**. To create a VM, follow the steps below:

Go to your Azure portal and in the search bar, type ``virtual`` and click on the first one.

![Resouce -group](images/from-code-to-k8s-images/images/vm.png)

Click on **``Create``**, then Click on **``Azure Virtual machine``**

![Resouce -group](images/from-code-to-k8s-images/images/click-on-azure-vm.png)


Fill the information as show below:

![Resouce -group](images/from-code-to-k8s-images/images/vm-setup1.png)

![Resouce -group](images/from-code-to-k8s-images/images/vm-setup2.png)

Leave everything as it is and click on **Tags**

Put in your tags, then click on **``Review + create``**.

![Resouce -group](images/from-code-to-k8s-images/images/vm-tag.png)

You will see all the information about your VM to be created. Click **Create**

![Resouce -group](images/from-code-to-k8s-images/images/validation-passed.png)

Now click on the **Download** button to download your RSA Key

![Resouce -group](images/from-code-to-k8s-images/images/download-rsa-key.png)

Click on **`` Go to resource ``**

![Resouce -group](images/from-code-to-k8s-images/images/go-to-resource.png)

Congratulations! You've successfully set up your VM. 

### 2a. Connect via SSH
To connect to the VM, click on **connect**, **connect**

![Resouce -group](images/from-code-to-k8s-images/images/click-on-connect.png)

We will connect to our VM using **Native SSH**. Click on **Select**

![Resouce -group](images/from-code-to-k8s-images/images/connect-to-vm.png)


Copy the command and paste it on your Notepad.

![Resouce -group](images/from-code-to-k8s-images/images/ssh-to-vm.png)

### 2b. Connect via CLI
- Create a folder on your PC and name it anything you like. Move the key you created into this folder. 
- Next, right-click on the folder and open it in a Command-line Interface (CLI). For example, I am using Git Bash in my case.

![Resouce -group](images/from-code-to-k8s-images/images/git-bash.png)

Type **ls** in your terminal, and you will see your key listed.

![Resouce -group](images/from-code-to-k8s-images/images/your-key.png)

Now to connect to your VM, paste the **``SSH command``** you copied earlier into the terminal. Replace **`` ~/.ssh/id_rsa.pem``** with your key as shown below.

![Resouce -group](images/from-code-to-k8s-images/images/replace-key.png)


Press **Enter** and type **yes** to confirm.

![Resouce -group](images/from-code-to-k8s-images/images/type-yes.png)

You have now successfully SSH into your VM from your CLI.

![Resouce -group](images/from-code-to-k8s-images/images/ssh-into-vm.png)

### 2c. Installing Docker
Run the command to install Docker on your VM

```sh
sudo apt update
sudo apt install docker.io -y
sudo usermod -aG docker therapiauser
sudo systemctl restart docker
sudo chmod 777 /var/run/docker.sock
```

Now, let's check if Docker is installed.

```sh
docker version
```

![Resouce -group](images/from-code-to-k8s-images/images/docker-version.png)

Congratulations on making it this far!

## Clone the repository

To build the image locally, first we will clone the repository and cd into the flask-app directory that contains the Dockerfile and use the commands to build the docker image. Run the commands below:


```sh
git clone https://github.com/Gerardbulky/azure-therapia.git
```

```sh
cd azure-therapia
```
Build Docker image:
```sh
docker build -t therapia-image:latest .
```
Run the Docker image using:
```sh
docker run -d -p 5000:5000 therapia-image:latest
```

Check if the docker image is running:
```sh
docker ps
```

<!-- ##### How It Works:
When you run a container with -p 5000:80, any traffic sent to port 5000 on the `` host `` will be forwarded to port 80 inside the container. 
**For example:**
    If the application is running inside the container on port 80, you can access it from your host machine via http://<<IP:address>>:5000  


![Ports](images/from-code-to-k8s-images/images/ports.png) -->



### Update Network Security Group Rules
In other to access our application over Port 5000, we need to update the NSG rules.

Go to **Virtual machines**, then go to **Networking** and click on **Network settings**.

![Network Settings](images/from-code-to-k8s-images/images/network-settings.png)

Click on **`` Create port rule ``** and select **`` Inbound rule ``**

![Inbound rule](images/from-code-to-k8s-images/images/inbound-rule.png)

Change the port to **5000**, protocol to **TCP** and click **Add**.

![Inbound port](images/from-code-to-k8s-images/images/inbound-port.png)

### Accessing the Application
Open your web browser and enter your Virtual Machine's IP address followed by port 5000, as shown below:

http://<<IP:address>>:5000

Good Job! You can now see your application on your web browser. Grab a cup of coffee while we move on to the next stage: Pushing image to ACR.

## Build & Push Image To Container Registry
Azure Container Registry(ACR) allows us to store, build and deploy images on Azure. We will need to create a registry to store our image.

We will need to install the Azure CLI to create our ACR account.

### 1. Install Azure CLI
On your terminal run the following command:

```sh
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

```sh
az login
```

Right-click, copy the **URL** and **code** and paste in your web browser. This will log you into your Azure account from your terminal.

![URL and Code](images/from-code-to-k8s-images/images/url-and-code.png)

You will be logged into your Azure account from the terminal. Press **Enter**

![Network Settings](images/from-code-to-k8s-images/images/logged-into-azure.png)

You are now logged into Azure from your CLI.

![Network Settings](images/from-code-to-k8s-images/images/logged-into-azure-from-cli.png)

### 2. Create Azure Registry

Replace the ``<container_registry_name>`` with a container name of your choice. It should be in **lowercase** and **no hyphen(-)** and is **unique**. For example, my container name is **therapiacontainer**, and if you choose to use a similar name, consider adding some characters to make yours unique, such as **therapiacontainer01**.

```sh
az acr create --resource-group therapia-resource \
              --name therapiaregistry \
              --sku Basic \
              --tags Name=therapia-tag
```
    
Your ACR is successfully created.

![Ports](images/from-code-to-k8s-images/images/acr-successfully-created.png)

To view your ACR, go to the Azure portal and on the search bar, type **container registries** and click on it.

![Ports](images/from-code-to-k8s-images/images/container-registry.png)

Click on your ACR. Copy the **login server url** and paste in on a note pad as you will need it later on.

![Ports](images/from-code-to-k8s-images/images/acr-login-url.png)


### 3. Build & Push Image To Container Registry 
Before pushing the image, we must authenticate with the Azure Container Registry(ACR). In the Azure CLI, run the command to log you into the ACR:

```sh
az acr login --name therapiaregistry
```
![Ports](images/from-code-to-k8s-images/images/login-succeeded.png)

Build the Image:

```sh
docker build -t therapiaregistry.azurecr.io/therapia-image:latest .
```
Push Image:
```sh
docker push therapiaregistry.azurecr.io/therapia-image:latest
```
To verify the image is created in your Azure Container Registry, run the command.

```sh
az acr repository list --name therapiaregistry --output table
```
![Ports](images/from-code-to-k8s-images/images/image-created-in-acr.png)

You should be proud of yourself for making it this far.
<!-- ## Push Image To DockerHub Registry
**1.  Log in to Docker Hub**
```sh
docker login
```
**2. Tag the Docker Image**
```sh
docker tag resume-app:latest bossmanjerry/resume-app:latest
```
**3. Push the Image**
```sh
docker push bossmanjerry/resume-app:latest
```
**4. Verify the Image on Docker Hub**
Log in to your Docker Hub account and check your repository to ensure the image is successfully uploaded. -->

## Deploying Image to AKS
To create an AKS cluster, you can follow the steps below.
If you're experienced with Azure, you can skip the networking setup. If you're new to AKS or Azure, I recommend following each step to understand the related services better.

Go to your Azure portal and in the search bar, type ``kubernetes`` and click on the first one. 

![Ports](images/from-code-to-k8s-images/images/kubernetes-search.png)

Click on **Create**, then **Kubernetes cluster**.

![kubernetes cluster](images/from-code-to-k8s-images/images/kubernetes-cluster.png)

Select your **resource group name**, add a **cluster name**. Click on **Next**.


![Cluster setup](images/from-code-to-k8s-images/images/cluster-setup.png)


In the **Node pools**, Provide the name of the **Node pool** and click on **update**.

![Ports](images/from-code-to-k8s-images/images/kubernetes-node-setup.png)


In the **Networking**, Select **kubelet** and **Calico** as Network policy.

![Ports](images/from-code-to-k8s-images/images/networking-setup.png)

Now go to **Tags**, select your tag and click on **Review + Create**.

![Ports](images/from-code-to-k8s-images/images/tag-setup.png)

Check your resources and click **Create**.

![Ports](images/from-code-to-k8s-images/images/create-k8s-cluster.png)

Once your deployment is complete, click on **Go to resource**.

![Ports](images/from-code-to-k8s-images/images/go-to-resource.png)

Congratulations on setting up an AKS Cluster.


<!-- Click on **Connect**.

![Ports](images/from-code-to-k8s-images/images/connect-to-cluster.png) -->


### 1. Install Kubectl
We need to install kubectl to connect the cluster to the terminal. In your terminal, run the following commands:

```sh
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.28.3/2023-11-14/bin/linux/amd64/kubectl
```

![Ports](images/from-code-to-k8s-images/images/kubectl-install1.png)


```sh
curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.28.3/2023-11-14/bin/linux/amd64/kubectl.sha256
```

![Ports](images/from-code-to-k8s-images/images/kubectl-install2.png)


```sh
sha256sum -c kubectl.sha256
```

![Ports](images/from-code-to-k8s-images/images/kubectl-install3.png)

```sh
chmod +x ./kubectl
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH
echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
```

![Ports](images/from-code-to-k8s-images/images/kubectl-install4.png)

```sh
kubectl version --client
```

![Ports](images/from-code-to-k8s-images/images/kubectl-version.png)


### 2. Connect Azure AKS to CLI
Go to your Azure cluster portal. Click on **Connect**
From your CLI, run both commands to connect to AKS.

![Ports](images/from-code-to-k8s-images/images/connect-to-cluster.png)

![Ports](images/from-code-to-k8s-images/images/connect-to-aks.png)


Now, you can run the command to list the nodes.


```sh
kubectl get nodes
```

![Ports](images/from-code-to-k8s-images/images/kubectl-get-nodes.png)


### 3. Grant AKS Access to ACR
We need to grant the AKS cluster access to pull the image from the ACR. Run the following command:

```sh
az aks update -n therapia-cluster -g therapia-resource --attach-acr therapiaregistry
```

![Access granted to AKS](images/from-code-to-k8s-images/images/access-granted-to-aks.png)

To Verify that the AKS cluster can pull images from ACR, run the following command:

```sh
az acr list --resource-group therapia-resource --query "[].{acrLoginServer:loginServer}" --output table
```

![registry-login-server](images/from-code-to-k8s-images/images/acr-name.png)



## Deploy Application yaml
Now, let’s try to deploy the containerised application on AKS.

From your terminal, 

```sh
nano deployment.yaml
```

Paste the code snippet. Replace  ``<container-registry-name>`` with your ACR name.

```sh
apiVersion: apps/v1
kind: Deployment
metadata:
  name: therapia-deployment
  labels: 
    app: therapia-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: therapia-app
  template: 
    metadata:
      labels:
        app: therapia-app
    spec:
      containers:
      - name: therapia-container
        image: therapiaregistry.azurecr.io/therapia-image:latest
        ports:
        - containerPort: 5000
```
##### In Windows:

Press **Ctrl + x** to exit

Press **y**, then **Enter**

```sh
kubectl apply -f deployment.yaml
```

![registry-login-server](images/from-code-to-k8s-images/images/kubectl-apply.png)


```sh
kubectl get pods
```

![registry-login-server](images/from-code-to-k8s-images/images/kubectl-get-pods.png)


Now, Let's host the application outside the Kubernetes Cluster by creating a service for the application.

```sh
nano service.yaml
```


```sh
apiVersion: v1
kind: Service
metadata:
  name: therapia-service
spec:
  selector:
    app: therapia-app
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 5000
```

##### In Windows:
Press **Ctrl + x** to exit

Press **y**, then **Enter**

```sh
kubectl apply -f service.yaml
```
![registry-login-server](images/from-code-to-k8s-images/images/service.png)

```sh
kubectl get svc
```

![registry-login-server](images/from-code-to-k8s-images/images/external-ip.png)

Copy the **EXTERNAL-IP** address, paste it into your favorite browser, and add port **5000** to view your application live.

![registry-login-server](images/from-code-to-k8s-images/images/application-live.png)

Congratulations on making it this far! This brings us to the end of this tutorial and I hope you found it helpful

## Conclusion
In this tutorial, we have walked through the comprehensive process of deploying a containerized application on Azure Kubernetes Service (AKS). Starting from setting up the necessary Azure resources, creating a virtual machine, building and pushing a Docker image to Azure Container Registry (ACR), and finally deploying the application on AKS, you have gained hands-on experience with various Azure services and tools. By following these steps, you should now be able to manage and deploy your applications effectively on AKS. Keep exploring and experimenting with Azure to further enhance your cloud skills. Happy coding!