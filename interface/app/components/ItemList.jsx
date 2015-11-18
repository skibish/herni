import React from 'react';
import Item from './Item.jsx';

class ItemList extends React.Component {
  constructor(props) {
    super(props);

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(event) {
    console.log('this is clicked', event.target);
    this.props.onItemSelection();
  }

  render() {
    var itemNodes = this.props.products.map((product) => {
      let isSelectable = (product.count > 0);
      return (
        <Item
          key={product.slot}
          name={product.name}
          price={product.price}
          count={product.count}
          isSelectable={isSelectable}
          onSelectClick={this.handleClick} />
        );
    });

    return (
      <div className="items">
        {itemNodes}
      </div>
    );
  }
}

export default ItemList;
