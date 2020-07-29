import React, {useState, useEffect} from 'react';
import { useId } from '@uifabric/react-hooks';
import {
  getTheme,
  mergeStyleSets,
  FontWeights,
  DefaultButton,
  Modal,
  IconButton,
  initializeIcons,
  PrimaryButton,
} from 'office-ui-fabric-react';
import {variableHandling} from './utils'
import AttributeList from './AttributeList'
import axios from 'axios'
import "./componentCss/Modal.css"
import AttributeListItem from './AttributeListItem';


const cancelIcon = { iconName: 'Cancel' };

export default ({id,data, RGName, hideModal, isModalOpen, onRouteGroupNameChange}) => {
  initializeIcons('https://static2.sharepointonline.com/files/fabric/assets/icons/')
  const findStartCount = (arrOfStrings) => {
    let arrOfNumbers = arrOfStrings.map(ele => {
      return Number(ele);
    })
    return Math.max(...arrOfNumbers);
  }

  const [count, setCount] = useState(Math.max(Object.keys(data))+1);
  const [deletedAttr, setDeletedAttr] = useState([])
  const [modalRGName, setModalRGName] = useState(RGName)
  const [attributeListItemArr, setAttributeListItemArr] = useState(data);
  const [userCreatedRG, setUserCreatedRG] = useState([])
  useEffect( () => {
    const startingCount = (findStartCount(Object.keys(data))) === -Infinity ? 0 : findStartCount(Object.keys(data));
    setAttributeListItemArr(data)
    setCount(startingCount + 1 || 0)
    setModalRGName(RGName)
    setDeletedAttr([])
}, [data, RGName])

  // Use useId() to ensure that the IDs are unique on the page.
  // (It's also okay to use plain strings and manually ensure uniqueness.)
  const titleId = useId('title');
  const theme = getTheme();

const contentStyles = mergeStyleSets({
  container: {
    display: 'flex',
    flexFlow: 'column nowrap',
    alignItems: 'stretch',
    width: '65%',
    maxWidth: '921px'
  },
  header: [
    theme.fonts.xLargePlus,
    {
      flex: '1 1 auto',
      borderTop: `4px solid ${theme.palette.themePrimary}`,
      color: theme.palette.neutralPrimary,
      display: 'flex',
      alignItems: 'center',
      fontWeight: FontWeights.semibold,
      padding: '12px 12px 14px 24px',
    },
  ],
  body: {
    flex: '4 4 auto',
    padding: '0 24px 24px 24px',
    overflowY: 'hidden',
    selectors: {
      p: { margin: '14px 0' },
      'p:first-child': { marginTop: 0 },
      'p:last-child': { marginBottom: 0 },
    },
  },
  footer: {
      display: "flex",
      justifyContent: "flex-end",
      margin: "20px"
  }
});
const iconButtonStyles = {
  root: {
    color: theme.palette.neutralPrimary,
    marginLeft: 'auto',
    marginTop: '4px',
    marginRight: '2px',
  },
  rootHovered: {
    color: theme.palette.neutralDark,
  },
};
  const addAttributeButtonOnClick = () => {
    const attributeListItemArrClone = JSON.parse(JSON.stringify(attributeListItemArr))
    attributeListItemArrClone[count] = {"name":"", "type": ""};
    setAttributeListItemArr(attributeListItemArrClone)
    setCount(count + 1);
  }

  const onChangeAttribute = (id, name, type) => {
    const attributeListItemArrClone = JSON.parse(JSON.stringify(attributeListItemArr))
    attributeListItemArrClone[id] = {"name": variableHandling(name), "type": type };
    setAttributeListItemArr(attributeListItemArrClone)
  }

  const deleteAttributeButtonOnClick = (id) => {
    setDeletedAttr(prevState => [...prevState, id]);
    const attributeListItemArrClone = JSON.parse(JSON.stringify(attributeListItemArr))
    delete attributeListItemArrClone[id];
    
    setAttributeListItemArr(attributeListItemArrClone);
  }

  const onClickModalSave = async (rgName) => {
    const userId = localStorage.getItem('userId');
    const modifiedRgName = variableHandling(rgName);
    const updatedRouteGroup = {"userId":userId, "objectName":modifiedRgName, "apiId":0, "isCRUD":true, "isReadMultiple":true, "isReadAllObjects":true, "isSingleRoute":true}
    const objectId = id;
    if(objectId >= 0 ){
      onRouteGroupNameChange({"id":objectId, "objectName" : modifiedRgName, "apiId": 0, "attributes": attributeListItemArr})
      await axios.post('/updateRouteGroup', {"objectId": objectId, "updatedRouteGroup": updatedRouteGroup})
      await axios.post('/updateMultipleObjectAttributes', {userId, deletedAttr, objectId, "attributes": attributeListItemArr})
    }else{
      let addedRG = await axios.post("/addNewRouteGroup", updatedRouteGroup);
      const addedRGID = addedRG.data.objectId
      onRouteGroupNameChange({"id":addedRGID, "objectName" : modifiedRgName, "apiId": 0, "attributes": attributeListItemArr})
      await axios.post('/updateMultipleObjectAttributes', {userId, deletedAttr, "objectId":addedRGID, "attributes": attributeListItemArr})
    }
    hideModal();
  }
  

  return (
    <div>
      <Modal
        titleAriaId={titleId}
        isOpen={isModalOpen}
        onDismiss={hideModal}
        isBlocking={true}
        containerClassName={contentStyles.container}
        dragOptions={false}
      >
        <div className={contentStyles.header}>
          <input type="text" id="routeGroupName" className="modalRouteGroupTitle" name="routeGroupName" onChange={(e) => {setModalRGName(e.target.value)}} value={modalRGName} placeholder="Enter Route Group Name" />
          <IconButton
            styles={iconButtonStyles}
            iconProps={cancelIcon}
            ariaLabel="Close popup modal"
            onClick={hideModal}
          />
        </div>
        <hr />
        <div className={contentStyles.body}>
          <div className="modalAddNewAttributeList">
            <AttributeList attributeListItemArr={attributeListItemArr} onChangeAttribute={onChangeAttribute} addAttributeButtonOnClick={addAttributeButtonOnClick} deleteAttributeButtonOnClick={deleteAttributeButtonOnClick}/>
          </div>
        </div>
        <hr />
        <div className={contentStyles.footer}>
            <PrimaryButton onClick={() => {onClickModalSave(modalRGName)}} className="modalAddNewAttributeSaveButton" text="Save" allowDisabledFocus /> 
            <DefaultButton text="Close" allowDisabledFocus  onClick={hideModal} />
        </div>
      </Modal>
    </div>
  );
};

