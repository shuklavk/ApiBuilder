import React, {useState, useEffect} from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Landing from './Landing';
import ViewApi from './ViewApi';
import Navbar from './Navbar'
import {validateUser, grabFakeUser, variableHandling} from './utils'
import axios from 'axios'

function App() {

  const [arrayOfRouteGroups, setArrayOfRouteGroups] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [apiName, setApiName] = useState("");
  
  useEffect (() => {
    async function fetchRouteGroups() {
      if(!await validateUser()){
        await grabFakeUser();
      }
      let routes = await axios.post('/viewAvailableRouteGroups', {"userId": localStorage.getItem('userId')})
      let currentApiName = await axios.post("/getAPIName", {"userId": localStorage.getItem('userId')})
      setApiName (currentApiName.data.api_name)
      setArrayOfRouteGroups(routes.data.groups)
      setIsLoading(false)
    }
    fetchRouteGroups()
  }, [])

  const onRouteGroupNameChange = async (RG) => {
    const arrayOfRGClone = arrayOfRouteGroups.slice();
    let foundRG = false;
    arrayOfRGClone.forEach((routeGroup) =>{
      if(routeGroup.id === RG.id ){
        routeGroup.objectName = RG.objectName;
        routeGroup.attributes = RG.attributes;
        foundRG = true;
      }
    })
    if(foundRG){
      setArrayOfRouteGroups(arrayOfRGClone)
    }else{
      setArrayOfRouteGroups(prevState => 
        [...prevState, RG]
      )
    }
  }

  const onRouteGroupDelete = async (rgName) => {
    const deletedRGInArray = arrayOfRouteGroups.filter(routeGroup => {
      return routeGroup.objectName !== rgName
    })
    setArrayOfRouteGroups(deletedRGInArray)
    // Need to find id from the db (any new RG added has a local id of -1)
    let currentRoute = await axios.post("/getRouteGroup", {"userId":localStorage.getItem('userId'), "filters": {"objectName":rgName}})
    const currentRouteId = currentRoute.data.id;
    await axios.post("/deleteRouteGroup", {"userId": localStorage.getItem('userId'), "objectId":currentRouteId})
  }

  const setApiNameOnClick = async (newApiName) => {
    await axios.post("/setAPIName", {'userId': localStorage.getItem('userId'), "apiName": newApiName})
  }

  let renderedPage;
  if(!isLoading){
    if (apiName !== ""){
      renderedPage = <ViewApi setApiNameOnClick={setApiNameOnClick} setApiName={setApiName} apiName={apiName} onRouteGroupDelete={onRouteGroupDelete} onRouteGroupNameChange={onRouteGroupNameChange} arrayOfRouteGroups={arrayOfRouteGroups}/>
    }else{
      renderedPage = <Landing setApiNameOnClick={setApiNameOnClick} apiName={apiName} setApiName={setApiName}/>
    }
  }
  else{
    renderedPage = <h1></h1>
  }
  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <Navbar />
          {renderedPage}
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
