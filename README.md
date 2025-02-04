# ArgoCD Repository

This repository contains the configuration files and manifests for deploying applications using ArgoCD.

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction
ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes. This repository helps you manage your Kubernetes applications with ArgoCD.

## Prerequisites
- Kubernetes cluster
- ArgoCD installed on the cluster
- kubectl configured to interact with your cluster

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/argocd-repo.git
    cd argocd-repo
    ```

2. Apply the ArgoCD manifests:
    ```sh
    kubectl apply -f manifests/
    ```

## Usage
1. Sync the application:
    ```sh
    argocd app sync <app-name>
    ```

2. Check the application status:
    ```sh
    argocd app get <app-name>
    ```

## Installation Vault

Run the below command to start the vault in the background
```sh
    nohup vault server -dev -dev-listen-address="0.0.0.0:8200" > vault.log 2>&1 &
```

To access the vault from the console, you need to have a Token which is stored in the vault.log file that is created by running on above command
  ```sh
    cat vault.log | tail -10
```

Now, Access the Vault GUI by copying the Public IP of the Vault Server with port 8200 and pasting the copied Root token

Now, export the vault address by running the below command
  ```sh
    export VAULT_ADDR='http://0.0.0.0:8200'
```

Now, enable the approle to create the role
 ```sh
    vault auth enable approle
```
Create a named role:
```sh
    vault write auth/approle/role/jenkins-role token_num_uses=0 secret_id_num_uses=0 policies="jenkins"
```

Fetch the RoleID of the AppRole:
```sh
 vault read auth/approle/role/jenkins-role/role-id
```

Get a SecretID issued against the AppRole:
```sh
vault write -f auth/approle/role/jenkins-role/secret-id
```

Create Secrets in Vault
Enable Secrets where path = “secrets” and it will using key value pair
```sh
 vault secrets enable -path=secrets kv
```

Write a Secret in Vault at path “secrets/cred/my-secret-text” with key as secret and value as jenkins123
```sh
 vault write secrets/creds/my-secret-text secret=jenkins123
```
**Creating Policy**
We now create a policy to give permission to approle to retrieve secrets
```sh
 vi jenkins-policy.hcl
```
path "secrets/creds/*" {
    capabilities = ["read"]
}

```sh
 vault policy write jenkins jenkins-policy.hcl
```
We created a policy named “jenkins” and use “jenkins-policy.hcl” as its content.


## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.