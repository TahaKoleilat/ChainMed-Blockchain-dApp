pragma solidity >=0.7.0 <0.9.0;
contract ChainMed{

    address Admin = address(0);
    // This declares a new complex type which will
    // be used for variables later.
    // It will represent a single patient
    struct Patient {
        // Card ID number given to doctor once registered in hospital
        uint256 patientID;
        //represents number of medical records a patient is allowed to upload. 
        //This is set by a registered doctor
        uint256 filesAllowed;   
        // represents the public key in the blockchain for the patient
        address patientAddress; 
    }

    struct Doctor {
        //Name of doctor that the patient wants to contact
        string doctorName;
        string doctorSurname;
        // Card ID number given to doctor once registered
        uint256 doctorID;
        // represents the public key in the blockchain for the doctor
        address doctorAddress; 
    }

    mapping(bytes32 => Patient) public patientMap; //add patient instance to dictionary indexed by a 256 bit hash
    mapping(bytes32 => Doctor) public doctorMap; //dictionary for all registered doctors in the healthcare organization
    mapping(bytes32=>bytes32[]) public ipfsMap; //Hash of IPFS File stored in encrypted form
    
    constructor() {
        require(msg.sender == Admin, "You are not authorized to deploy a contract!");
    }
    
    function registerDoctor(uint256 _doctorID,string memory _doctorName,string memory _doctorSurname, address _doctorAddress) external{
        require(msg.sender == Admin, "You are not authorized!");
        require(doctorMap[sha256(abi.encodePacked(_doctorAddress))].doctorAddress == address(0), "Doctor is already registered!");
        doctorMap[sha256(abi.encodePacked(_doctorAddress))] = Doctor({doctorName: _doctorName,doctorSurname: _doctorSurname,
        doctorID: _doctorID,doctorAddress: _doctorAddress});
    }
    
    function registerPatient(uint256 _patientID,address _patientAddress) external{
        require(msg.sender == Admin, "You are not authorized!");
        require(patientMap[sha256(abi.encodePacked(_patientAddress))].patientAddress == address(0), "Patient is already registered!");
        patientMap[sha256(abi.encodePacked(_patientID,_patientAddress))] = Patient({patientID: _patientID,filesAllowed: 0,
        patientAddress:_patientAddress});
    }

    function uploadFile(bytes32 _ipfshash,address _doctorAddress,address _patientAddress) external{
        require(msg.sender == _patientAddress || msg.sender == _doctorAddress, "Unauthorized identity!");
        require(patientMap[sha256(abi.encodePacked(_patientAddress))].patientID != 0, "Patient is not registered!");
        require(doctorMap[sha256(abi.encodePacked(_doctorAddress))].doctorID != 0, "Doctor is not registered!");
        ipfsMap[sha256(abi.encodePacked(_patientAddress,_doctorAddress))].push(_ipfshash);
    }

    function retrieveFile(address _doctorAddress,address _patientAddress) public view returns (bytes32[] memory){
        require(msg.sender == _patientAddress || msg.sender == _doctorAddress, "Unauthorized identity!");
        require(patientMap[sha256(abi.encodePacked(_patientAddress))].patientID != 0, "Patient is not registered!");
        require(doctorMap[sha256(abi.encodePacked(_doctorAddress))].doctorID != 0, "Doctor is not registered!");
        return(ipfsMap[sha256(abi.encodePacked(_patientAddress,_doctorAddress))]);
    }

    function setFileAllowed(address _doctorAddress,address _patientAddress,uint256 _filesAllowed) external{
        require(msg.sender == _doctorAddress || msg.sender == Admin, "You are not authorized!");
        require((patientMap[sha256(abi.encodePacked(_patientAddress))]).patientID != 0, "Patient is not registered!");
        require((doctorMap[sha256(abi.encodePacked(_doctorAddress))]).doctorID != 0, "Doctor is not registered!");
        patientMap[sha256(abi.encodePacked(_patientAddress))].filesAllowed = _filesAllowed;
    }

    function removePatient(address _patientAddress) external{
        require(msg.sender == Admin, "You are not authorized!");
        require((patientMap[sha256(abi.encodePacked(_patientAddress))]).patientID != 0, "No such entity exists!");
        delete patientMap[sha256(abi.encodePacked(_patientAddress))];
    }

    function removeDoctor(address _doctorAddress) external{
        require(msg.sender == Admin, "You are not authorized!");
        require((doctorMap[sha256(abi.encodePacked(_doctorAddress))]).doctorID != 0, "No such entity exists!");
        delete doctorMap[sha256(abi.encodePacked(_doctorAddress))];
    }

}