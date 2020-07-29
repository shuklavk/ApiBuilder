import React from 'react';
import CurrentApisListItem from './CurrentApisListItem';
import './componentCss/CurrentApisList.css'

export default () => {
  const arr = []
  for(let i = 0; i < 7; i++){
      arr.push(<CurrentApisListItem className="currentApisListItem1" index={i}/>)
  }

  return (
    <div className='currentApisListDiv'>
        {arr}
    </div>
  );
};
