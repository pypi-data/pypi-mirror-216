import time
import datetime
import json
import requests

from davi_bot_api_consumer.exceptions_davi import ProposalAlreadyAssignedError, ProposalNotOnExpectedStatusError, ApiDaviErro

class STATUS_RA:
    APROVADO='ap'
    NAO_APROVADO='na'
    ERRO='er'
    ATUAR='at'

class BancosFebraban:
    PAN = '623'
    BMG = '318'
    ITAU = '029'
    OLE = '169'
    BANRISUL = '041'
    DAYCOVAL = '707'
    C6 = '336'
    BRADESCO = '237'


class RiskAnalysis:
    ''' A class to represents a model of the ParceiroVIP system. '''
    id : int
    bankCode : int
    userId : int
    covenant : str
    cpf : str
    status : str
    value : str
    parcelValue : float
    amountParcel : int
    bankStore : int
    createdAt : datetime
    updatedAt : datetime
    aprovedAt : datetime
    aproved : bool
    finishedAt :datetime
    robot : bool
    userIdAgent : int
    proposalAde : str
    clientName : str
    proposalProduct : str
    representativeId : int
    statusInternal : str
    typistUser : str
    robotAttempts : int
    promoterAnalysis : str
    manualActionRobotNotApproved : bool
    manualActionNotLinked : bool
    representativeSubStore : int
    ra_use_id : str

    def __init__(self, ra_json: dict):
        TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

        self.id = ra_json['id']
        self.bankCode = ra_json['bankCode']
        self.userId = ra_json['userId']
        self.covenant = ra_json['covenant']
        self.cpf = ra_json['cpf']
        self.status = ra_json['status']
        self.value = ra_json['value']
        self.parcelValue = ra_json['parcelValue']
        self.amountParcel = ra_json['amountParcel']
        self.bankStore = ra_json['bankStore']
        self.createdAt = ra_json['createdAt'] if not(ra_json['createdAt']) else datetime.datetime.strptime(ra_json['createdAt'],TIME_FORMAT)
        self.updatedAt = ra_json['updatedAt'] if not(ra_json['updatedAt']) else datetime.datetime.strptime(ra_json['updatedAt'],TIME_FORMAT)
        self.aprovedAt = ra_json['aprovedAt'] if not(ra_json['aprovedAt']) else datetime.datetime.strptime(ra_json['aprovedAt'],TIME_FORMAT)
        self.aproved = ra_json['aproved']
        self.finishedAt = ra_json['finishedAt'] if not(ra_json['finishedAt']) else datetime.datetime.strptime(ra_json['finishedAt'],TIME_FORMAT)
        self.robot = ra_json['robot']
        self.userIdAgent = ra_json['userIdAgent']
        self.proposalAde = ra_json['proposalAde']
        self.clientName = ra_json['clientName']
        self.proposalProduct = ra_json['proposalProduct']
        self.representativeId = ra_json['representativeId']
        self.statusInternal = ra_json['statusInternal']
        self.typistUser = ra_json['typistUser']
        self.robotAttempts = ra_json['robotAttempts']
        self.promoterAnalysis = ra_json['promoterAnalysis']
        self.manualActionRobotNotApproved = ra_json['manualActionRobotNotApproved']
        self.manualActionNotLinked = ra_json['manualActionNotLinked']
        self.representativeSubStore = ra_json['representativeSubStore']
        self.ra_use_id = ra_json['ra_use_id']
        
    def __repr__(self):
        return f"Proposal [{self.proposalAde}]"

    def __dict__(self):
        return {
            "id": self.id,
            "bankCode": self.bankCode,
            "userId": self.userId,
            "covenant": self.covenant,
            "cpf": self.cpf,
            "status": self.status,
            "value": self.value,
            "parcelValue": self.parcelValue,
            "amountParcel": self.amountParcel,
            "bankStore": self.bankStore,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
            "aprovedAt": self.aprovedAt,
            "aproved": self.aproved,
            "finishedAt": self.finishedAt,
            "robot": self.robot,
            "userIdAgent": self.userIdAgent,
            "proposalAde": self.proposalAde,
            "clientName": self.clientName,
            "proposalProduct": self.proposalProduct,
            "representativeId": self.representativeId,
            "statusInternal": self.statusInternal,
            "typistUser": self.typistUser,
            "robotAttempts": self.robotAttempts,
            "promoterAnalysis": self.promoterAnalysis,
            "manualActionRobotNotApproved": self.manualActionRobotNotApproved,
            "manualActionNotLinked": self.manualActionNotLinked,
            "representativeSubStore": self.representativeSubStore,
            "ra_use_id": self.ra_use_id,
        }

    def __repr__(self):
        return f"Proposal [{self.proposalAde}]"

    def __dict__(self):
        return {
            "id": self.id,
            "bankCode": self.bankCode,
            "userId": self.userId,
            "covenant": self.covenant,
            "cpf": self.cpf,
            "status": self.status,
            "value": self.value,
            "parcelValue": self.parcelValue,
            "amountParcel": self.amountParcel,
            "bankStore": self.bankStore,
            "createdAt": self.createdAt.strftime('%Y-%m-%d %H:%M:%S') if self.createdAt else None,
            "updatedAt": self.updatedAt.strftime('%Y-%m-%d %H:%M:%S') if self.updatedAt else None,
            "aprovedAt": self.aprovedAt.strftime('%Y-%m-%d %H:%M:%S') if self.aprovedAt else None,
            "aproved": self.aproved,
            "finishedAt": self.finishedAt.strftime('%Y-%m-%d %H:%M:%S') if self.finishedAt else None,
            "robot": self.robot,
            "userIdAgent": self.userIdAgent,
            "proposalAde": self.proposalAde,
            "clientName": self.clientName,
            "proposalProduct": self.proposalProduct,
            "representativeId": self.representativeId,
            "statusInternal": self.statusInternal,
            "typistUser": self.typistUser,
            "robotAttempts": self.robotAttempts,
            "promoterAnalysis": self.promoterAnalysis,
            "manualActionRobotNotApproved": self.manualActionRobotNotApproved,
            "manualActionNotLinked": self.manualActionNotLinked,
            "representativeSubStore": self.representativeSubStore,
            "ra_use_id": self.ra_use_id,
        }

class PartnerEmailListNotFound(Exception):
    def __init__(self, partner_code: str):
        super().__init__(f"Erro ao consultar emails do parceiro {partner_code}")
        self.partner_code = partner_code
class UnkownPartnerEmailListFetchException(Exception):
    def __init__(self, partner_code: str, response_content: any):
        super().__init__(f"Erro desconhecido ao consultar emails do parceiro {partner_code}")
        self.partner_code = partner_code
        self.response_content = response_content

class Client:
    name: str
    cpf: str

    def __init__(self, name, cpf):
        self.name = name
        self.cpf = cpf

    def __repr__(self):
        return f"Client [{self.cpf}]"

class Proposal:

    davi_id: str
    box_id: str
    bank_id: str
    bank_name: str
    status: str
    number: int
    product: str
    covenant: str
    typer: str
    inserted_at: datetime
    updated_at: datetime  
    client : Client  
    promoter_name: str
    promoter_id: str
    
    def __init__(self, proposal_json: dict, bank_name: str):
        TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
        
        self.davi_id = proposal_json['id']
        self.box_id = proposal_json['boxId']
        self.bank_id = proposal_json['bankId']
        self.bank_name = bank_name
        self.status = proposal_json['status']
        self.number = proposal_json['number']
        self.product = proposal_json['product']
        self.covenant = proposal_json['covenant']
        self.typer = proposal_json['typer']
        self.inserted_at = datetime.datetime.strptime(proposal_json['insertedAt'], TIME_FORMAT)
        self.updated_at = datetime.datetime.strptime(proposal_json['updatedAt'], TIME_FORMAT)
        self.client = Client(
            name= proposal_json['client']['name'],
            cpf= proposal_json['client']['cpf']
        )
        self.promoter_name = proposal_json['promoter']['name']
        self.promoter_id = proposal_json['promoter']['id']

    def __repr__(self):
        return f"Proposal [{self.number}]"

    def __dict__(self):
        return {
           "davi_id" : self.davi_id,
           "box_id" : self.box_id,
           "bank_id" : self.bank_id,
           "bank_name" : self.bank_name,
           "status" : self.status,
           "number" : self.number,
           "product" : self.product,
           "covenant" : self.covenant,
           "typer" : self.typer,
           "inserted_at" : self.inserted_at.strftime('%Y-%m-%d %H:%M:%S'),
           "updated_at" : self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
           "client_cpf" : self.client.cpf,
           "client_name" : self.client.name,
           "promoter_name" : self.promoter_name,
           "promoter_id" : self.promoter_id
        }



class ApiDavi:
    """ A interface to communicate with Davi system from Fontes.
    Manages itself the jwt token refresh, requires the following os.environ keys:
    >>> os.environ['DAVI_USER']
    >>> os.environ['DAVI_PASS']
    >>> os.environ['DAVI_USER_ID']
    """

    def __init__(
        self,
        API_URL: str,
        AUTH_URL: str,
        DAVI_USER: str,
        DAVI_PASS: str,
        DAVI_USER_ID: str,
        token_file_path: str

    ):
        self.API_URL = API_URL
        self.AUTH_URL = AUTH_URL
        self._DAVI_USER = DAVI_USER
        self._DAVI_PASS =  DAVI_PASS
        self._DAVI_USER_ID =    DAVI_USER_ID
        self._jwt_token = None
        self._token_valid_until = None
        self.token_file_path = token_file_path

    @property
    def authorization_header(self) -> dict:
        r"""Returns the authorization header with the jwt token. Logon to DAVI if needed
        :rtype: dict"""

        def get_saved_token():
            with open('services/davi/token.json', 'r') as f:
                j = json.loads(f.read())
                j['expires_in'] = datetime.datetime.strptime(j['expires_in'], '%Y-%m-%d %H:%M')
                return j
        
        def save_token():
            with open('services/davi/token.json', 'w') as f:
                j = {
                    'token': self._jwt_token,
                    'expires_in': self._token_valid_until.strftime('%Y-%m-%d %H:%M')
                }
                f.write(json.dumps(j))
            
        def auth_nextflow():
            url = f"{self.AUTH_URL}/service-account/login/nextflow"
            requests.options(url)

            payload = {"clientId": self._DAVI_USER, "secret": self._DAVI_PASS}
            response = requests.post(url, data=payload)
            
            if response.status_code != 200:
                raise ApiDaviErro(f"Conteudo: {response.content} código: {response.status_code}" )

            data = response.json()

            self._jwt_token = data["token"]
            self._token_valid_until = datetime.datetime.now() + datetime.timedelta(hours=4)

        if self._jwt_token is None:
            try:
                j = get_saved_token()
            except FileNotFoundError:
                j = None

            if j:
                self._token_valid_until = j['expires_in']
                if self._token_valid_until > datetime.datetime.now():
                    self._jwt_token = j['token']
                    return {
                        'Authorization': f'Bearer {self._jwt_token}'
                    }
            auth_nextflow()
            save_token()
        elif self._token_valid_until < datetime.datetime.now():
            auth_nextflow()
            save_token()
        return {
            'Authorization': f'Bearer {self._jwt_token}'
        }
    def get_proposals_to_work(self, banco_id: str, box_id: str) -> dict:
        """Gets an proposals to work to the given bank_name. Returns None if no tasks avaiable.

        :param bank_name: str bank name to get the task
        :rtype: `ProposalTask`

        :raises InexistentBankError: if the bank_name does not exists.
        """
        url = f"https://davi-api.fontespromotora.com.br/proposals?showOnStandardTreadmill=true&statuses[]=awaiting-analysis&inReanalysis=false&inProgress=false&boxId={box_id}&bankId={banco_id}&page=1&size=1000&sortBy=priority&sortDirection=asc"
        headers = self.authorization_header
        payload={}

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 400:
            raise ApiDaviErro(response.text)
        elif response.status_code == 200 or response.status_code==206:
            if response.json() == { }:
                return None
            return response.json()
        else:
            raise ApiDaviErro(response.text)

    def assign_proposal(self, proposal: Proposal, change_to_in_progress: bool = True) -> None:
        """Change an proposal status to assigned ou unassigned based on change_to_in_progress.
        :param proposal: `Proposal` proposal to be assigned or unassigned
        :change_to_in_progress: bool wheter to assign or unassign the `Proposal` object

        :raises ProposalNotOnExpectedStatusError: when the proposal is not on status 'awaiting-analysis'
        :raises ProposalAlreadyAssignedError: when the proposal is already in progress if tries to assign it
        """
        davi_proposal = self.get_proposal(proposal['id'])
        if davi_proposal['status'] != 'awaiting-analysis':
            if change_to_in_progress:
                raise ProposalNotOnExpectedStatusError()
            return

        url = f"{self.API_URL}/proposals/{proposal['id']}/assignment"
        requests.options(url, headers=self.authorization_header)

        headers = self.authorization_header
        headers.update({'Content-Type': 'application/json'})
        payload = {'assignedTo': self._DAVI_USER_ID, 'inProgress': change_to_in_progress}

        response = requests.patch(url, data=json.dumps(payload), headers=headers)

        print(f"URL: {url} | Status Code: {response.status_code} | Additional Data: Assigned inProgress: {change_to_in_progress} {proposal['number']}")
        print(f"Assigned inProgress: {change_to_in_progress} {proposal['number']} Status Code: {response.status_code}")

        if response.status_code != 204:
            if response.status_code == 401 and change_to_in_progress:
                raise ProposalAlreadyAssignedError(response.text)
            else:
                raise ApiDaviErro(response.text)

    def approve_proposal(self, proposal: Proposal) -> None:
        """Approve an proposal.
        :param proposal: `Proposal` proposal to be approved
        
        :raises Exception: when status code is not 204.
        """
        url = f"{self.API_URL}/proposals/{proposal['id']}/status"
        requests.options(url, headers=self.authorization_header)

        payload = {"status": "approved", "motive": "Análise Aprovada"}
        headers = self.authorization_header
        headers.update({'Content-Type': 'application/json'})

        for _ in range(10):
            try:
                response = requests.patch(url, headers=headers, data=json.dumps(payload))
            except ApiDaviErro:
                time.sleep(3)
                continue
            
            if response.status_code != 204:
                raise ApiDaviErro(f'Ocorreu um erro ao finalizar proposta no davi. Código: {response.status_code} erro: {response.json()} ')
            break
        print(f"URL: {url} | Status Code: {response.status_code} | Additional Data: Approved {proposal['number']}")
        print(f"Approved {proposal['number']} Status Code: {response.status_code}")

    def pending_proposal(self, proposal: Proposal, motive = "Análise Pendenciada") -> None:
        """Pending an proposal with motive: Proposal not found and submotive: [].
        :param proposal: `Proposal` proposal to be pending
        """
        url = f"{self.API_URL}/proposals/{proposal['id']}/pendency"
        requests.options(url, headers=self.authorization_header)

        payload = json.dumps({
          "motive": motive,
          "pendencyMotiveId": "6250344fb3f3d50012519170", # Robot Pendency Box Id
          "pendencySubMotiveIds": [],
          "analysisPhases": []
        })
        
        headers = self.authorization_header
        headers.update({'Content-Type': 'application/json'})
        response = requests.patch(url, headers=headers, data=payload)
        print(f"URL: {url} | Status Code: {response.status_code} | Additional Data: Pending {proposal['number']}")
        print(f"Pending {proposal['number']} Status Code: {response.status_code}")
##---------------------------------------- TESTE ----------------------------------------------

    def get_proposals_with_pendencies(self, bank_id: str, pendency_id: str, page: int = 1, size: int = 100) -> list:
        '''Return an list of dict of proposals on queue to the given params: bank_id and pendency_id'''
        url = f'{self.API_URL}/proposals?showOnStandardTreadmill=true&statuses[]=pending&inReanalysis=false&inProgress=false&inImportProgress=false'
        url += f'&pendencyMotiveId={pendency_id}&bankId={bank_id}&page={page}&size={size}&sortBy=priority&sortDirection=asc'

        headers=self.authorization_header
        headers.update({'Content-Type': 'application/json'})
        response = requests.get(url, headers=headers)
        json_response = response.json()

        return json_response
    
    def set_proposal_to_pending(self, proposal_id: str, pendency_id: str, motive: str) -> requests.Response:
        '''Sets an proposal_id to pending as an pendency_id and motive'''
        url = f'{self.API_URL}/proposals/{proposal_id}/pendency'
        payload = {
            'analysisPhases': [],
            'motive': motive,
            'pendencyMotiveId': pendency_id,
            'pendencySubMotiveIds': [],
        }
        requests.options(url, headers=self.authorization_header)

        headers = self.authorization_header
        headers.update({'Content-Type': 'application/json'})
        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        return response


    def get_all_banks(self) -> list:
        """Returns an list of all banks registered on davi.
        :rtype: list[dict]
        """

        url = f'{self.API_URL}/banks'
        response = requests.get(url, headers=self.authorization_header)
        return response.json()



    def get_all_boxes(self) -> list:
        """Returns an list of all boxes registered on davi.
        :rtype: list[dict]
        """
        url = f'{self.API_URL}/boxes'
        response = requests.get(url, headers=self.authorization_header, params={'size':200})
        return response.json()



    def get_pendency_motives(self) -> list:
        '''Returns an list of dict of all pendency motives'''
        url = f'{self.API_URL}/pendency-motives/search?page=1&size=100&sortBy=defaultSort&sortDirection=asc&statuses[]=active'
        requests.options(url, headers=self.authorization_header)

        response = requests.get(url, headers=self.authorization_header)
        json_response = response.json()

        return json_response

    def get_pendency_motive_by_name(self, name: str) -> dict:
        '''Returns an dict of an pendency by the given param name. Returns `{ }` if none found.'''
        pendencys = self.get_pendency_motives()
        for pendency in pendencys:
            if pendency['name'].upper() == name.upper():
                return pendency
        return { }


    def assign_pending_proposal_by_id(self, proposal_id: str, change_to_in_progress: bool = True) -> None:
        '''Sets an proposal as assigned.'''
        url = f"{self.API_URL}/proposals/{proposal_id}/assignment"
        requests.options(url, headers=self.authorization_header)

        headers = self.authorization_header
        headers.update({'Content-Type': 'application/json'})
        payload = {'assignedTo': self._DAVI_USER_ID, 'inProgress': change_to_in_progress}

        response = requests.patch(url, data=json.dumps(payload), headers=headers)
        return response
##---------------------------------------- TESTE ----------------------------------------------
    def refuse_proposal(self, proposal: Proposal, motive = "Análise Reprovada") -> None:
        """Refuses an proposal with motive: Bank and submotive: Bank Cancelled.
        :param proposal: `Proposal` proposal to be refused
        """
        url = f"{self.API_URL}/proposals/{proposal['id']}/disapproval"
        requests.options(url, headers=self.authorization_header)

        payload = {
            "motive": motive,
            "disapprovalMotiveId": "5e1f1c40d1138100122ee6a2", #Banco
            "disapprovalSubMotiveIds": ["5e1f1c9ef6a76500119fd45b"] #Cancelado Banco
        }
        
        headers = self.authorization_header
        headers.update({'Content-Type': 'application/json'})
        response = requests.patch(url, headers=headers, data=json.dumps(payload))
        print(f"URL: {url} | Status Code: {response.status_code} | Additional Data: Refused {proposal['number']}")
        print(f"Refused {proposal['number']} Status Code: {response.status_code}")

    def get_proposal(self, davi_id: str) -> dict:
        """Returns an dict with the proposal data to the given davi_id.
        :param davi_id: str id of the proposal to search
        :rtype: list[`Proposal`]
        """
        url = f"{self.API_URL}/proposals/{davi_id}"
        requests.options(url, headers=self.authorization_header)

        response = requests.get(url, headers=self.authorization_header)
        return response.json()

    def get_proposal_golias(self, bank_id: str, golias_url:str, loja: str ="") -> dict:
        """Retorna propostas em massa do Golias
        :param bank_id: Id do banco como está no Davi
        :param loja: A loja referente ao acesso
        :param golias_url: A URL do Golias
        """
        if loja=="":
            url = f"{golias_url}/proposta/banco/{bank_id}"
        else:
            url = f"{golias_url}/proposta/banco/{bank_id}/loja/{loja}"

        requests.options(url, headers=self.authorization_header)

        response = requests.get(url, headers=self.authorization_header)
        propostas= response.json()
        propostas_davi=[]
        for proposta in propostas:
            proposta_davi=self.get_proposal(proposta.get('id_proposta_davi'))
            propostas_davi.append(proposta_davi)
        
        return propostas_davi

    def get_partner_email_list(self, partner_code: str):
                '''Sets an proposal as assigned.'''
                url = f'{self.API_URL}/partner-emails/partner/{partner_code}'
                requests.options(url, headers=self.authorization_header)
                headers = self.authorization_header
                headers.update({'Content-Type': 'application/json'})
                
                response = requests.get(url, headers=headers)
                        
                return response.json()

class ApiParceiroVip:
    ''' Classe da api para manipulação de propostas do
    sistema ParceiroVIP.
    >>> URL da API
    '''
    def __init__(
        self,
        URL_PARCEIRO_VIP: str,
        BANCO: str,
        LOJA: str
    ):
        self.URL_PARCEIRO_VIP = URL_PARCEIRO_VIP
        self.BANCO = BANCO
        self.LOJA = LOJA

    def get_proposal_parceiro_vip(self, action:str):
        '''Retorna as propostas analisadas no sistema Parceiro VIP
        :url_parceiro_vip: Endereço da api Parceiro VIP
        :banco: Banco das propostas solicitadas
        :store: Loja das propostas solicitas
        :action: Ação das propostas solicitadas (aprovacao/reprovacao) '''
        url = f'{self.URL_PARCEIRO_VIP}/api/v2/robot/{self.BANCO}/{self.LOJA}/{action}'
        headers={'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and response.json():
            return [RiskAnalysis(ra) for ra in response.json()]
        else:
            return []

    def update_status_parceiro_vip(self, ra: RiskAnalysis, status:str):
        '''Retorna as propostas analisadas no sistema Parceiro VIP
        :url_parceiro_vip: Endereço da api Parceiro VIP
        :status: Novo status para atualização
        :ra: Proposta a ser modificada'''
        url = f'{self.URL_PARCEIRO_VIP}/api/v2/robot/{ra.id}/{status}'
        headers = {'Content-Type': 'application/json'}
        
        response = requests.patch(url, headers=headers)    
    
        print(response.text)

    def conversor_ra (self, ra: RiskAnalysis) -> dict:
        return dict({
            "number": ra.proposalAde,
            "convenant": ra.covenant,
            "client":{
                "cpf" : ra.cpf
            }
        })

    def approve_proposal_vip(self, aprove_class):
        proposals=self.get_proposal_parceiro_vip('aprovacao')
        for proposal in proposals:
            try:
                #TODO Desfazer mock 
                aprove_class.aprovacao(self.conversor_ra(proposal))
                print('Proposta aprovada com sucesso' + str(proposal.__dict__()))
                self.update_status_parceiro_vip(proposal, STATUS_RA.APROVADO)
            except:
                self.update_status_parceiro_vip(proposal,STATUS_RA.ATUAR)

    def cancel_proposal_vip(self, cancel):
        proposals=self.get_proposal_parceiro_vip('cancel')
        for proposal in proposals:
            try:
                cancel(self.conversor_ra(proposal))
                self.update_status_parceiro_vip(proposal, STATUS_RA.NAO_APROVADO)
            except:
                self.update_status_parceiro_vip(proposal, STATUS_RA.ATUAR)

