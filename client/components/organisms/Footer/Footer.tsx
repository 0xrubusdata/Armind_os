// components/organisms/Footer/Footer.tsx
import styles from '../../../styles/Footer.module.css';

interface FooterProps {
    copyrightText: string; // The copyright text to display in the footer
}

const Footer: React.FC<FooterProps> = ({ copyrightText }) => {
    return (
        <footer className={styles.footer}>
            <p>{copyrightText}</p>
        </footer>
    );
};

export default Footer;