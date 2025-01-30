// pages/_app.tsx
import { AppProps } from 'next/app';
import Head from 'next/head';
import '../styles/globals.css';
import Layout from '../components/Layout';
import React from 'react';

const MyApp = ({ Component, pageProps }: AppProps) => {
    return (
        <>
            <Head>
                <title>ArmindOS - AI Agents Framework</title>
                <link rel="icon" href="/icons8-favicon-16.ico" />
                <meta name="description" content="Framework for agents AI development." />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
            </Head>
            <Layout>
                <Component {...pageProps} />
            </Layout>
        </>
    );
};

export default MyApp;