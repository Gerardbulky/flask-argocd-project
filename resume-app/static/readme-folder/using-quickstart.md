# Exposing Kibana service externally using Nginx Ingress & Cert Manager

This guide will show you how to set up Cert-Manager and NGINX Ingress on Kubernetes to automate TLS certificate management with Let’s Encrypt.
**Ingress** is a Kubernetes resource that manages external access to services within a cluster, typically HTTP and HTTPS traffic.
**Cert-Manager** automates the process of obtaining and renewing TLS certificates from providers like Let’s Encrypt. It integrates seamlessly with Ingress controllers (e.g., NGINX) to handle certificate management automatically.

##### Step 1: Create a Namespace

First, let's create a dedicated namespace for the Ingress controller:

```sh
kubectl create namespace ingress-basic 
```
##### Step 2. Installing Helm
Helm is a package manager for Kubernetes that simplifies the deployment and management of applications. First, we’ll install Helm.

```sh
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```
Verify the installation:

```sh
helm version
```
##### Step 3.  Installing NGINX Ingress Controller
The NGINX Ingress Controller manages HTTP and HTTPS traffic within Kubernetes. We’ll install it using Helm.

Add the Helm repository:
```sh
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
```
![Running Pods](images/nginx.png)

Before running the next command, Go to Azure Account search for Azure Load Balancer, and click on it.

![Loadbalancer](images/loadbalancer.png)

There can be many load balancers if you have created if the load balancer name is Kubernetes click on it.

![Loadbalancer page](images/loadbalancer-page.png)
Once you land on the Kubernetes load balancer page, Click on Frontend IP Configuration and copy the IP address.

![IP Address](images/ip-address.png)

Next, install the Helm chart using the command below. Be sure to replace ``<PUBLIC-IP>`` with the Public IP address you copied in the earlier steps.

```sh
helm install ingress-nginx ingress-nginx/ingress-nginx \
    --namespace ingress-basic \
    --set controller.replicaCount=2 \
    --set controller.nodeSelector."kubernetes\.io/os"=linux \
    --set defaultBackend.nodeSelector."beta\.kubernetes\.io/os"=linux \
    --set controller.service.externalTrafficPolicy=Local \
    --set controller.service.loadBalancerIP="<PUBLIC-IP>"

```

![Cert Manager Installed](images/cert-manager-installed.png)

To check if Ingress is installed, run the following command and ensure all pods are running.

![Running Pods](images/validate-pods-running.png)

Next, we’ll configure an SSL certificate for our application, which will be deployed within the next hour.

Run the following command to label ingress-basic for validation:
```sh
kubectl label namespace ingress-basic cert-manager.io/disable-validation=true
```

![Ingress Validation](images/Ingress-validation.png)

Add the cert manager helm repo and update the repo
```sh
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

![Cert Manager Repo](images/cert-manager-repo.png)


To configure SSL for our application, we need to create Custom Resource Definitions (CRDs). 

Run the following command:
```sh
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.7.1/cert-manager.crds.yaml
```

![Custom Cert Manager](images/custom-cert-manager.png)


Install the cert manager helm chart

```sh
helm install cert-manager jetstack/cert-manager \
  --namespace ingress-basic \
  --version v1.7.1
```

![Custom Cert Manager Installed](images/custom-manager-installed.png)

Validate whether cert-manager pods are running or not

![Custom Cert Manager Installed](images/validate-all-pods-running.png)


#### Step 4. Cluster Issuer Configuration
In this step, we’ll set up the Cluster Issuer, which handles SSL certificate management for our application.

##### Issuer (issuer.yaml)

```sh
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
 name: letsencrypt
spec:
 acme:
   server: https://acme-v02.api.letsencrypt.org/directory
   email: <your-email-address.com> # You must replace this email address with your own. Let's Encrypt will use this to contact you when your cert is about to expire.
   privateKeySecretRef:
    name: letsencrypt 
   solvers:
   - http01:
       ingress:
         class: nginx
         podTemplate:
           spec:
             nodeSelector:
               "kubernetes.io/os": linux
```

Run the following command:
```sh
kubectl apply -f issuer.yaml
```

#### Step 5. Ingress Configuration

At this stage, we will update the ingress file by adding annotations and configuring TLS settings.

```sh
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingresslb
  namespace: elk  # Make sure this matches the namespace of your configuration files'
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt
    nginx.ingress.kubernetes.io/proxy-read-timeout: "120"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "120"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - <Add-your-domain-name>
    secretName: tls-secret
  rules:
    - host: <Add-your-domain-name>
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: kibana
                port:
                  number: 5601
```

Run the following command:
```sh
kubectl apply -f ingress.yaml
```


##### Step 6: Verify Cert-Manager has issued a certificate:
The ``tls secret`` is the value of the ``secretName`` in the Ingress file

```sh
kubectl describe certificate tls-secret -n elk
```
![Ingress Validation](images/certificate-ready.png)

```sh
kubectl get cert
```
![Ingress Validation](images/cert-true.png)


##### Step 7: Verify ingress:

```sh
kubectl get ingress -n elk
```

![Ingress Validation](images/ingress.png)

I've added the public IP provided by Ingress on my domain provider.

![DNS Records](images/dns-record.png)

Hit the hostname from your browser, and you should see the Kibana dashboard.

Congratulations! You have successfully deployed the ELK Stack to your AKS cluster with HTTPS enabled.

![Kibana Dashboard](images/kibana-dashboard-empty.png)

## Conclusion

This structure provides a comprehensive guide for deploying the ELK Stack (Elasticsearch, Kibana, and Logstash) on Azure AKS using YAML configuring files and ensuring security best practices for production environments.

For more detailed configurations and customizations, refer to the official [Elastic Helm Charts documentation](https://github.com/elastic/helm-charts).


## Contact
If you have questions or would like to discuss further, feel free to reach out to me or connect me directly on my [LinkedIn Profile](https://www.linkedin.com/in/gerard-ambe-80050b152/).


