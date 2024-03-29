node {
    
    stage('Checkout SCM'){
        checkout scm
    }

    DockerRepositoryAddress='docker.io'
    DockerImageName='flask-demo'
    DockerImageTag='latest'

    stage('Build App Image') {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
            sh """
                docker login ${DockerRepositoryAddress} -u $DOCKER_USER -p $DOCKER_PASSWORD
                docker build -t ${DockerRepositoryAddress}/${DOCKER_USER}/${DockerImageName}:${DockerImageTag} ./image/
                docker push     ${DockerRepositoryAddress}/${DOCKER_USER}/${DockerImageName}:${DockerImageTag}
            """
        }
    }

    jenkinsAgentDockerfileName = 'agent.dockerfile'
    jenkinsAgentBuildName = 'agent:latest'
    jenkinsAgentBuildArgs = ''
    jenkinsAgentRunArgs = " -u 0:0"
    def RunAgent = docker.build("${jenkinsAgentBuildName}", "${jenkinsAgentBuildArgs} -f ${jenkinsAgentDockerfileName} .")

    app_name="flask-app"
    app_namespace="flask-ns"
    app_service_port_number="80"
    container_port="5000"
    ingress_host="flask-app.local.com"

    stage('Deploy to Openshift'){
        withCredentials([
                        usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD'),
                        file(credentialsId: 'k8s-config', variable: 'K8S_CONFIG')
                        ]){
                            RunAgent.inside("${jenkinsAgentRunArgs}") {
                                sh  """
                                    mkdir -p ~/.kube
                                    cat ${K8S_CONFIG} > ~/.kube/config
                                    helm upgrade ${app_name} helm/ -n ${app_namespace} \
                                    --set imageCredentials.registry=${DockerRepositoryAddress} \
                                    --set imageCredentials.username=${DOCKER_USER} \
                                    --set imageCredentials.password=${DOCKER_PASSWORD} \
                                    --set container.image=${DockerRepositoryAddress}/${DOCKER_USER}/${DockerImageName}:${DockerImageTag} \
                                    --set container.port=${container_port} \
                                    --set service.port.port_number=${app_service_port_number} \
                                    --set ingress.host=${ingress_host} \
                                    --create-namespace \
                                    --install
                                    """
                }
            }
        }

    stage('Clear'){
        deleteDir()
        }
    
}