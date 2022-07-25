node('master'){
    
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
    app_namespace="helm-demo"

    stage('Deploy to Openshift'){
        withCredentials([
                        usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD'),
                        file(credentialsId: 'oc-config', variable: 'OC_CONFIG')
                        ]){
                            RunAgent.inside("${jenkinsAgentRunArgs}") {
                                sh  """
                                    mkdir -p ~/.kube
                                    cat ${OC_CONFIG} > ~/.kube/config
                                    helm install ${app_name} helm/ -n ${app_namespace} \
                                    --set container.image=${DockerRepositoryAddress}/${DOCKER_USER}/${DockerImageName}:${DockerImageTag}
                                    """
                }
            }
        }

    stage('Clear'){
        deleteDir()
        }
    
}