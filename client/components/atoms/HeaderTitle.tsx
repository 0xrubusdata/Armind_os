import React from 'react';

interface HeaderTitleProps {
  title: string;
}

const HeaderTitle: React.FC<HeaderTitleProps> = ({ title }) => {
  return <h1>{title}</h1>;
};

export default HeaderTitle; 