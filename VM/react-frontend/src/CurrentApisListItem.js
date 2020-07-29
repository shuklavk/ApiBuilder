import React from 'react';
import { Card} from '@uifabric/react-cards';
import { FontWeights } from '@uifabric/styling';
import { Icon, Stack, Text, initializeIcons } from 'office-ui-fabric-react';


export default ({index}) => {
    initializeIcons('https://static2.sharepointonline.com/files/fabric/assets/icons/')

    const alertClicked = () => {
      alert('Clicked');
    };

    const siteTextStyles = {
        root: {
          color: '#0F6EBE',
          fontWeight: FontWeights.semibold,
          fontSize: '20px',
          cursor: "pointer",
        },
      };
      const descriptionTextStyles= {
        root: {
          color: '#000000',
          fontWeight: FontWeights.regular,
          fontSize: '15px',
          cursor: "auto"
        },
      };
      const iconStyles = {
        root: {
          color: '#0078D4',
          fontSize: 20,
          fontWeight: FontWeights.regular,
          cursor: 'pointer',
          paddingTop: '5px',
          paddingBottom: '20px'
        },
      };

      const extraOptionsIconStyles = {
        root: {
          color: '#0078D4',
          fontSize: 20,
          fontWeight: FontWeights.regular,
          cursor: 'pointer'
        },
      };
      const footerCardSectionStyles = {
        root: {
          alignSelf: 'stretch',
          borderLeft: '1px solid #F3F2F1',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        },
      };
  
      const sectionStackTokens = { childrenGap: 1 };
      const cardTokens = { childrenMargin: 12};
      const footerCardSectionTokens = { padding: '0px 0px 0px 12px' };
  
      return (
        <Stack tokens={sectionStackTokens}>
          <Card aria-label="Clickable horizontal card " horizontal  tokens={cardTokens} style={{justifyContent:"space-between", marginTop:"20px", marginBottom:"20px" ,width:'430px', height:"190px"}}>
            <Card.Section >
              <Text variant="medium" styles={siteTextStyles} onClick={alertClicked}>
                Facebook Messenger API
              </Text>
              <Text styles={descriptionTextStyles}>Build lasting customer relationships through conversation. Messenger from Facebook allows you to connect with over 1.3 billion people in a channel they prefer - making business personal and convenient. </Text>
            </Card.Section>
            <Card.Section styles={footerCardSectionStyles} tokens={footerCardSectionTokens}>
              {/* <Icon iconName="SingleBookmark" styles={iconStyles} onClick={(e) => {
                  e.preventDefault()
                  console.log('clicked bookmark')
                  }}/> */}
                  <div>
                    <Icon iconName="Edit" styles={iconStyles} />
                    <Icon iconName="Delete" styles={iconStyles} />
                  </div>
                  <div>
                      <Icon iconName="More" styles={extraOptionsIconStyles} />
                  </div>
              {/* <Stack.Item grow={1}>
                <span />
              </Stack.Item> */}
            </Card.Section>
          </Card>
        </Stack>
      );
     
}