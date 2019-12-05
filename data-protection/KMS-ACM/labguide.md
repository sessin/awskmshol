# 랩 가이드
 이 Workshop 은 AWS에서 제공하는 암호화 솔루션을 이용하여 데이터를 암호화/복호화하는 방법을 손쉽게 따라함으로써 고객의 이해를 돕는데 그 목적이 있습니다. 랩을 진행하는데 있어 보다 편리하고 동일한 사용환경을 제공하기 위하여 AWS Management Console 과 함께 Cloud9 IDE 를 사용합니다.
 
# 데이터 암호화
 데이터 암호화는 여러분이 AWS서비스를 이용하면서 저장하는 데이터에 대한 강력한 보호 수단을 제공합니다. AWS 서비스는 고객의 선택에 따라 데이터를 저장하거나 전송하는 동안 데이터를 암호화할 수 있는 방안을 제공합니다.

# 사전 요구 사항
### AWS 계정
이 lab 을 진행하기 위해서는 "admin" 권한을 가지고 있는 AWS 계정이 필요합니다. Lab 을 진행하는 각 과정의 코드와 지시 항목들은 모두 Lab 을 진행하는 사람이 해당 권한을 가지고 있다는 것을 전제하고 있습니다.

반드시 기존에 사용하던 개별적인 AWS 계정을 사용하거나 별도의 AWS 계정을 생성하는 것을 권고하며 회사 업무에서 사용하는 계정을 사용하는 것은 권고하지 않습니다.

만일, Lab 을 진행한 후 삭제되지 않고 남아 있는 리소스가 있는 경우 해당 리소스로 인한 과금이 발생할 수 있습니다. 따라서, Lab 종료 후 반드시 리소스를 삭제하시기 바랍니다.

### 브라우저
이 Lab 은 Cloud9 IDE 를 사용하는 것을 전제합니다. 따라서, Lab 의 원활한 진행을 위해 최신 버전의 Chrome 이나 FireFox 를 사용하는 것을 권고합니다.

### Region 선택
이 Lab 은 Cloud9 IDE 를 사용하기 때문에 이 Lab 의 진행을 위해서는 Cloud9 이 지원되는 Region 을 선택하여야합니다.
Cloud9 지원 Region
**N.Virginia, Ohio, Oregon, Ireland and Singapore.**
 
### 초기 환경 설정 CloudFormation 템플릿
Lab 진행에 필요한 환경을 준비하기 위하여 아래의 CloudFormation Stack 을 실행하기 바랍니다.

### Step 1 :

[![Deploy IAM user creation stack](images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=data-protection-iam-user-creation&templateURL=https://s3.amazonaws.com/crypto-workshop-dont-delete/template-create-user.yaml)

이 Stack 은 **builder** 라는 IAM 사용자를 생성하며 암호는 **awskorea** 로 설정되어 있습니다.

### Step 2 를 시작하기 전에
**builder** IAM 사용자 자격증명을 이용하여 로그인 후 암호를 변경하시기 바랍니다.

### Step 2 :

[![Deploy workshops environment creation stack](images/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=data-protection-env-setup&templateURL=https://s3.amazonaws.com/crypto-workshop-dont-delete/template-env-setup.yaml)

위 Stack 은 **workshop-environment** 라는 이름의 Cloud9 IDE 를 생성하며, 2개의 Subnet 과 Internet Gateway 와 VPC 를 생성합니다.

### Step 3 :
* AWS Management Console 에 로그인 후 Cloud9 서비스로 이동합니다.

* **workshop-environment** 라는 이름의 Cloud9 IDE 환경을 선택합니다. 선택된 환경이 시작하는데까지 약 30초의 시간이 소요될 수 있습니다.
* Cloud9 IDE 환경에 접속한 후 화면 좌측의 폴더 화면에서 **data0protection** 이라는 이름의 폴더가 있는 것을 확인합니다.

* IDE 에서 **environment-setup.py** 를 엽니다. 

* 실행 버튼을 클릭하여 **environment-setup.py** 파이썬 모듈을 실행합니다.
 
* 이 모듈은 완료시까지 약 1분이 소요됩니다.

* 화면 하단의 runner window 에서 **Workshop environment setup was successful** 가 출력된 것을 확인할 수 있습니다.

* 여기까지 진행되었다면 Lab 진행을 위한 Cloud9 환경이 준비된 것입니다.