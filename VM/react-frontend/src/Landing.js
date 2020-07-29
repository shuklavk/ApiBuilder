import React from 'react';
import NewApiStep from './NewApiStep'

export default ({apiName, setApiName, setApiNameOnClick}) => {
  return (
    <div>
      <NewApiStep apiName={apiName} setApiName={setApiName} setApiNameOnClick={setApiNameOnClick}/>
      </div>
  );
};
