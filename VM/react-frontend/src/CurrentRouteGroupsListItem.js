import React from 'react';
import { Card} from '@uifabric/react-cards';
import { IconButton, Stack, Text, initializeIcons } from 'office-ui-fabric-react';


export default ({onRouteGroupDelete, setRGName, setId, id, RGName ,data, setData, showModal}) => {

    initializeIcons('https://static2.sharepointonline.com/files/fabric/assets/icons/')
    
    const routeGroupStackStyles = {
        root: {
          flexDirection: "row",
        },
    };

    const menuProps = {
        items: [
          {
            key: 'editRG',
            text: 'Edit Route Group',
            iconProps: { iconName: 'Edit' },
            onClick: () => {RGTextOnClick()}
          },
          {
            key: 'deleteRG',
            text: 'Delete Route Group',
            iconProps: { iconName: 'Delete' },
            onClick: () => {onRouteGroupDelete(RGName)}
          },
        ],
        directionalHintFixed: true,
    };
    
    const routeGroupCardStyles = {
        root: {
            width:'-webkit-fill-available',
            maxWidth: "none",
            justifyContent:"space-between",
            marginTop: "15px",
            marginBottom: "15px",
        },
    };
    const routeGroupIconStyles = {
        root: {
            marginTop:'auto',
            marginBottom: "auto",
            marginRight:"5px",
        },
        icon: {
            fontSize: "20px"
        }
    };
    const routeGroupTextStyles = {
        root: {
            fontSize: '20px',
            cursor: "pointer"
        },
    };

    const sectionStackTokens = { childrenGap: 8 };
    const cardTokens = { childrenMargin: 12 };

    const RGTextOnClick = () => {
        setData(data)
        setRGName(RGName)
        setId(id)
        showModal();
    }

    return(
        <div>
            <Stack tokens={sectionStackTokens} styles={routeGroupStackStyles}>
                <Card aria-label="Basic horizontal card" styles= {routeGroupCardStyles} horizontal tokens={cardTokens}>
                    <Card.Item>
                        <Text styles={routeGroupTextStyles} onClick={RGTextOnClick}>{RGName}</Text>
                    </Card.Item>
                    <IconButton menuProps={menuProps}  styles={routeGroupIconStyles} title="Options" ariaLabel="Options" />
                </Card>
            </Stack>
        </div>
    )
}