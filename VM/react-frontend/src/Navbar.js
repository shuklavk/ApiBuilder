import React from 'react';
import './componentCss/Navbar.css';
import LogoImage from './LogoImage'
import LogoText from './LogoText'
import BlogLink from './BlogLink'
import TutorialLink from './TutorialLink'
import AllAPIsLink from './AllAPIsLink'

export default () => {
  return (
    <header className="NavbarHeader">
      <ul className="navbarUl">
        <div className="navbarLogoDiv">
          <LogoImage/>
          <LogoText/>
        </div>
        <nav className="navbarNav" id="navlinks">
            <BlogLink/>
            <TutorialLink/>
            <AllAPIsLink/>
        </nav>
      </ul>
    </header>

  );
}

