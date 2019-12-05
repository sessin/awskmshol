+++
title = "실습 안내"
weight = 1
pre = "<b>1.1 </b>"
+++
* * *
# 실습 가이드
 이 실습은 AWS에서 제공하는 KMS(Key Management Service)를 이용하여 데이터를 암호화/복호화하는 방법을 손쉽게 따라함으로써 고객의 이해를 돕는데 그 목적이 있습니다. 실습을 진행하는데 있어 보다 편리하고 동일한 사용환경을 제공하기 위하여 AWS Management Console 과 함께 Cloud9 IDE 를 사용합니다.
 
# 데이터 암호화
 데이터 암호화는 여러분이 AWS서비스를 이용하면서 저장하는 데이터에 대한 강력한 보호 수단을 제공합니다. AWS 서비스는 고객의 선택에 따라 데이터를 저장하거나 전송하는 동안 데이터를 암호화할 수 있는 방안을 제공합니다.

# 사전 요구 사항
### AWS 계정
이 실습을 진행하기 위해서는 "administrator" 권한을 가지고 있는 AWS 계정이 필요합니다. 실습을 진행하는 각 과정의 코드와 지시 항목들은 모두 실습을 진행하는 사람이 해당 권한을 가지고 있다는 것을 전제하고 있습니다.

반드시 기존에 사용하던 개별적인 AWS 계정을 사용하거나 별도의 AWS 계정을 생성하는 것을 권고하며 회사 업무에서 사용하는 계정을 사용하는 것은 권고하지 않습니다.

만일, 실습을 진행한 후 삭제되지 않고 남아 있는 리소스가 있는 경우 해당 리소스로 인한 과금이 발생할 수 있습니다. 따라서, 실습 종료 후 반드시 리소스를 삭제하시기 바랍니다.

### 브라우저
이 실습 은 Cloud9 IDE 를 사용하는 것을 전제합니다. 따라서, 실습의 원활한 진행을 위해 최신 버전의 Chrome 이나 FireFox 를 사용하는 것을 권고합니다.

### Region 선택
이 실습은 Cloud9 IDE 를 사용하기 때문에 이 실습의 진행을 위해서는 Cloud9 이 지원되는 Region 을 선택하여야합니다.

{{% notice info %}}
2019년 12월 기준 Cloud9 지원 Region = 
**N.Virginia, Ohio, Oregon, Ireland, Singapore, Tokyo.**
{{% /notice %}}
## 이번 실습은 AWS 도쿄(Tokyo) 리전에서 수행됩니다.
	
- [AWS 관리 콘솔](https://console.aws.amazon.com/)로 접속해서, 아래의 화면과 같이 AWS 도쿄 리전이 선택되었는지 확인합니다.
![Tokyo Region](/images/tokyo_region.png)
	 
***
### 초기 환경 설정 CloudFormation 템플릿
실습 진행에 필요한 환경을 준비하기 위하여 아래의 CloudFormation Stack 을 실행하기 바랍니다.

### Step 1 :

CloudFormation 템플릿을 실행하기 위해 [링크](https://eu-central-1.console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/create/review?templateURL=https://do-not-delete-eunsshin-workshop.s3.ap-northeast-2.amazonaws.com/kms/template-env-setup.yaml)를 클릭합니다.

아래와 같이 CloudFormation Stack 생성화면에서 이름을 입력하고 화면 하단의 체크박스를 선택한 후 "스택 생성" 버튼을 클릭하여 스택을 생성합니다.
![Stack Creation](/images/env_stack1.png)

스택 생성이 정상적으로 진행되면 아래와 같이 2개의 스택 생성이 완료된 것을 확인하실 수 있습니다. 위 스택은 workshop-environment라는 이름의 Cloud9 IDE 를 생성하며, 2개의 Subnet 과 Internet Gateway 와 VPC 를 생성합니다.
![Stack Createion](/images/two-stack.png)

CloudFormation 템플릿을 실행하기 위해 [링크](https://eu-central-1.console.aws.amazon.com/cloudformation/home?region=ap-northeast-1#/stacks/create/review?templateURL=https://do-not-delete-eunsshin-workshop.s3.ap-northeast-2.amazonaws.com/kms/template-create-user.yaml)를 클릭합니다.

![Stack Createion](/images/user-stack.png)

정상적으로 진행되었다면 아래와 같이 스택 생성이 완료된 것을 확인할 수 있습니다.
![Stack Createion](/images/user-stack-complete.png)
{{% notice note %}}
이 스택은 "builder" 라는 IAM 사용자를 생성하며 암호는 "AWSkorea2020!" 로 설정되어 있습니다.
{{% /notice %}}

{{% notice note %}}
builder IAM 사용자 자격증명을 이용하여 로그인 후 암호를 변경하시기 바랍니다.
{{% /notice %}}

### Step 2 :
* Administrator 권한을 가진 IAM 사용자를 이용하여 AWS Management Console 에 로그인 후 Cloud9 서비스로 이동합니다.
![Stack Createion](/images/cloud9service.png)
* workshop-environment 라는 이름의 Cloud9 IDE 환경을 선택합니다. 선택된 환경이 시작하는데까지 약 30초의 시간이 소요될 수 있습니다.
![Stack Createion](/images/cloud9.png)
* Cloud9 IDE 환경에 접속한 후 화면 좌측의 폴더 화면에서 data-protection 이라는 이름의 폴더가 있는 것을 확인합니다.
![Stack Createion](/images/cloud9-folder.png)
* IDE 에서 environment-setup.py 를 엽니다. 

* 실행 버튼을 클릭하여 environment-setup.py 파이썬 모듈을 실행합니다.
 
* 이 모듈은 완료시까지 약 1분이 소요됩니다.

* 화면 하단의 runner window 에서 **Workshop environment setup was successful** 가 출력된 것을 확인할 수 있습니다.

* 여기까지 진행되었다면 Lab 진행을 위한 Cloud9 환경이 준비된 것입니다.